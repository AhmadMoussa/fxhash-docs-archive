#!/usr/bin/env python3
"""Build the static website in docs/ from the Markdown archive in markdown/.

    pip install -r tools/requirements.txt
    python3 tools/build_site.py

The output is plain HTML/CSS/JS with relative links, so it works on GitHub Pages
(Settings -> Pages -> Deploy from branch -> /docs), on any static host, or opened
straight from disk.
"""
import html
import json
import os
import re
import shutil
import unicodedata

from markdown_it import MarkdownIt
from markdown_it.token import Token
from PIL import Image
from pygments import highlight as pyg_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

# ------------------------------------------------------------------ settings
SITE_NAME = "fxhash docs"
SITE_TAG = "archive"
OWNER_NAME = "Gorilla Sun"
OWNER_URL = "https://www.gorillasun.de/"
ORIGINAL_SITE = "https://docs.fxhash.xyz"
SNAPSHOT_URL = "https://web.archive.org/web/20260313230640/https://docs.fxhash.xyz/"
SNAPSHOT_LABEL = "13 March 2026"
IMAGE_MAX_WIDTH = 1600
IMAGE_QUALITY = 82

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_DIR = os.path.join(ROOT, "markdown")
OUT = os.path.join(ROOT, "docs")
TOOLS = os.path.join(ROOT, "tools")
TEMPLATE_DIR = os.path.join(TOOLS, "site")
CACHE = os.path.join(TOOLS, ".image-cache.json")


# ------------------------------------------------------------------ navigation (from SUMMARY.md)
def parse_summary():
    groups, current = [], {"label": None, "items": []}
    groups.append(current)
    stack = []
    for line in open(os.path.join(MD_DIR, "SUMMARY.md"), encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("## "):
            current = {"label": line[3:].strip(), "items": []}
            groups.append(current)
            stack = []
            continue
        m = re.match(r"^(\s*)\* \[(.+?)\]\((.+?)\)\s*$", line)
        if not m:
            continue
        depth = len(m.group(1)) // 2
        node = {"title": m.group(2), "href": m.group(3), "children": [], "group": current["label"]}
        stack = stack[:depth]
        (stack[-1]["children"] if stack else current["items"]).append(node)
        node["parent"] = stack[-1] if stack else None
        stack.append(node)
    return [g for g in groups if g["items"]]


def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n["children"])


def is_external(href):
    return bool(re.match(r"^[a-z]+:", href))


def site_dir(md_path):
    """markdown path -> site directory ('' for the root page, otherwise ending with '/')."""
    md_path = md_path.replace(os.sep, "/")
    if md_path == "README.md":
        return ""
    if md_path.endswith("/README.md"):
        return md_path[: -len("README.md")]
    return md_path[:-3] + "/"


def rel(from_dir, to_path):
    """Relative URL from a site directory to a site path (directory or file)."""
    r = os.path.relpath(to_path.rstrip("/") or ".", from_dir.rstrip("/") or ".").replace(os.sep, "/")
    if to_path.endswith("/") or to_path == "":
        return "./" if r == "." else r + "/"
    return r


# ------------------------------------------------------------------ front matter
def read_page(md_path):
    text = open(os.path.join(MD_DIR, md_path), encoding="utf-8").read()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).split("\n"):
            k, _, v = line.partition(":")
            v = v.strip()
            meta[k.strip()] = json.loads(v) if v.startswith('"') else v
        text = text[m.end():]
    # the page title / description are rendered from front matter, so drop their body copies
    h = re.match(r"\s*# (.+)\n", text)
    if h:
        meta.setdefault("title", h.group(1).strip())
        text = text[h.end():]
    desc = meta.get("description")
    if desc:
        text = re.sub(r"^\s*\*" + re.escape(desc) + r"\*\s*\n", "", text, count=1)
    return meta, text


# ------------------------------------------------------------------ images
def load_cache():
    try:
        return json.load(open(CACHE))
    except (OSError, ValueError):
        return {}


image_cache = load_cache()


def optimise_asset(name):
    """Copy/convert markdown/assets/<name> into docs/assets/; returns (site_path, width, height)."""
    src = os.path.join(MD_DIR, "assets", name)
    stem, ext = os.path.splitext(name)
    ext = ext.lower()
    if ext in (".mp4", ".webm", ".mov"):
        dest_rel = f"assets/media/{name}"
        dest = os.path.join(OUT, dest_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        return dest_rel, None, None
    keep = ext in (".gif", ".svg")
    dest_rel = f"assets/img/{name}" if keep else f"assets/img/{stem}.webp"
    dest = os.path.join(OUT, dest_rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    key = f"{name}:{os.path.getmtime(src)}"
    cached = image_cache.get(key)
    if cached and os.path.exists(dest):
        return dest_rel, cached[0], cached[1]
    if ext == ".svg":
        shutil.copy2(src, dest)
        w = h = None
    else:
        with Image.open(src) as im:
            w, h = im.size
            if keep:
                shutil.copy2(src, dest)
            else:
                if w > IMAGE_MAX_WIDTH:
                    h = round(h * IMAGE_MAX_WIDTH / w)
                    w = IMAGE_MAX_WIDTH
                    im = im.resize((w, h), Image.LANCZOS)
                if im.mode not in ("RGB", "RGBA"):
                    im = im.convert("RGBA")
                im.save(dest, "WEBP", quality=IMAGE_QUALITY, method=6)
    image_cache[key] = [w, h]
    return dest_rel, w, h


# ------------------------------------------------------------------ markdown rendering
LANG_LABELS = {"js": "JavaScript", "javascript": "JavaScript", "jsx": "JSX", "ts": "TypeScript",
               "typescript": "TypeScript", "html": "HTML", "css": "CSS", "bash": "Shell", "sh": "Shell",
               "shell": "Shell", "json": "JSON", "glsl": "GLSL", "python": "Python", "solidity": "Solidity",
               "yaml": "YAML", "xml": "XML", "csv": "CSV", "markdown": "Markdown"}
LEXER_FALLBACK = {"jsx": "javascript", "js": "javascript", "sh": "bash", "shell": "bash"}
FORMATTER = HtmlFormatter(nowrap=True)


def highlight_code(code, lang, _attrs):
    lang = (lang or "").strip().lower()
    body = html.escape(code)
    if lang:
        for name in (lang, LEXER_FALLBACK.get(lang)):
            if not name:
                continue
            try:
                body = pyg_highlight(code, get_lexer_by_name(name), FORMATTER)
                break
            except ClassNotFound:
                continue
    label = LANG_LABELS.get(lang, lang.upper() if lang else "")
    data = f' data-lang="{html.escape(label)}"' if label else ""
    return f'<pre class="code"{data}><code>{body.rstrip()}</code></pre>\n'


def slugify(text):
    """Approximates GitBook's heading ids so links to sections keep their original anchors."""
    t = unicodedata.normalize("NFKD", text)
    t = t.replace("&", " and ").replace("$", "usd").replace("’", "").replace("'", "")
    t = re.sub(r"[^a-z0-9.]+", "-", t.lower())
    t = re.sub(r"-+", "-", t).strip("-") or "section"
    return "id-" + t if t[0].isdigit() else t


HINT_LABELS = {"NOTE": ("note", "Info"), "TIP": ("tip", "Tip"), "WARNING": ("warning", "Warning"),
               "CAUTION": ("caution", "Danger"), "IMPORTANT": ("note", "Important")}
ICONS = {
    "note": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></svg>',
    "tip": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/></svg>',
    "warning": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2 20h20L12 3z"/><path d="M12 10v4M12 17h.01"/></svg>',
    "caution": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M15 9l-6 6M9 9l6 6"/></svg>',
}
ALLOWED_HTML = {"details", "summary", "br", "strong", "em", "code", "sup", "sub", "kbd", "mark", "b", "i"}


def trusted(content):
    t = Token("html_block", "", 0)
    t.content = content
    t.meta = {"trusted": True}
    return t


def embed_html(kind, url, env):
    esc = html.escape(url)
    if kind == "CodePen demo":
        m = re.match(r"https://codepen\.io/([^/]+)/(?:pen|embed)/([^/?#]+)", url)
        if m:
            user, pen = m.groups()
            return (f'<div class="embed embed-codepen"><iframe loading="lazy" title="CodePen demo {pen}" '
                    f'src="https://codepen.io/{user}/embed/{pen}?default-tab=result" allowfullscreen></iframe>'
                    f'<a class="embed-caption" href="https://codepen.io/{user}/pen/{pen}" target="_blank" rel="noopener">'
                    f'Open this demo on CodePen ↗</a></div>\n')
    if kind == "Video":
        m = re.search(r"(?:v=|youtu\.be/)([\w-]{6,})", url)
        if m:
            vid = m.group(1)
            return (f'<div class="embed embed-video"><iframe loading="lazy" title="YouTube video" '
                    f'src="https://www.youtube-nocookie.com/embed/{vid}" allowfullscreen '
                    f'allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"></iframe>'
                    f'<a class="embed-caption" href="{esc}" target="_blank" rel="noopener">Watch on YouTube ↗</a></div>\n')
    label = {"Post on X": "Post on X", "Video": "Video"}.get(kind, "Linked content")
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    return (f'<a class="embed-card" href="{esc}" target="_blank" rel="noopener"><span class="embed-kind">{label}</span>'
            f'<span class="embed-url">{html.escape(host)}{html.escape(url.split(host, 1)[-1][:70])}</span></a>\n')


def core_transform(state):
    env = state.env
    toks = state.tokens
    out = []
    i = 0
    callout_stack = []
    while i < len(toks):
        t = toks[i]
        # embeds:  > **CodePen demo:** <url>   /   > **Video:** [name](assets/x.mp4)
        if (t.type == "blockquote_open" and i + 4 < len(toks) and toks[i + 1].type == "paragraph_open"
                and toks[i + 2].type == "inline" and toks[i + 4].type == "blockquote_close"):
            m = re.match(r"^\*\*(CodePen demo|Video|Post on X|Embedded content):\*\* (?:<([^>]+)>|\[[^\]]*\]\(([^)]+)\))$",
                         toks[i + 2].content.strip())
            if m:
                kind, url, local = m.groups()
                if local:
                    target = resolve_md_target(env, local)
                    src = rel(env["dir"], env["assets"](target)[0])
                    out.append(trusted(f'<figure class="embed embed-file"><video controls preload="metadata" '
                                       f'src="{html.escape(src)}"></video></figure>\n'))
                else:
                    out.append(trusted(embed_html(kind, url, env)))
                i += 5
                continue
        # callouts:  > [!NOTE]
        if t.type == "blockquote_open" and i + 2 < len(toks) and toks[i + 2].type == "inline":
            m = re.match(r"^\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)\]\s*\n?", toks[i + 2].content)
            if m:
                cls, label = HINT_LABELS[m.group(1)]
                rest = toks[i + 2].content[m.end():]
                out.append(trusted(f'<div class="callout callout-{cls}" role="note" aria-label="{label}">'
                                   f'<span class="callout-icon">{ICONS[cls]}</span><div class="callout-body">\n'))
                callout_stack.append(t.level)
                if rest.strip():
                    inline = toks[i + 2]
                    inline.content = rest
                    inline.children = []
                    state.md.inline.parse(rest, state.md, env, inline.children)
                    out.extend(toks[i + 1:i + 4])
                i += 4
                continue
        if t.type == "blockquote_close" and callout_stack and callout_stack[-1] == t.level:
            callout_stack.pop()
            out.append(trusted("</div></div>\n"))
            i += 1
            continue
        # headings get stable ids
        if t.type == "heading_open" and i + 1 < len(toks):
            text = "".join(c.content for c in toks[i + 1].children or [] if c.type in ("text", "code_inline"))
            base = slugify(text)
            slug, n = base, 1
            while slug in env["ids"]:
                n += 1
                slug = f"{base}-{n}"
            env["ids"].add(slug)
            t.attrSet("id", slug)
            env["headings"].append((int(t.tag[1]), slug, text))
        out.append(t)
        i += 1
    # links (separate pass, so inline content re-parsed above is covered too)
    for t in out:
        for c in (t.children or []) if t.type == "inline" else []:
            if c.type != "link_open":
                continue
            href = c.attrGet("href") or ""
            if is_external(href):
                if not href.startswith("mailto:"):
                    c.attrSet("target", "_blank")
                    c.attrSet("rel", "noopener")
            elif not href.startswith("#"):
                c.attrSet("href", resolve_link(env, href))
    state.tokens = out


def resolve_md_target(env, href):
    from urllib.parse import unquote
    path = unquote(href.split("#")[0])
    return os.path.normpath(os.path.join(os.path.dirname(env["md"]), path)).replace(os.sep, "/")


def resolve_link(env, href):
    frag = "#" + href.split("#", 1)[1] if "#" in href else ""
    target = resolve_md_target(env, href)
    if target.endswith(".md"):
        return rel(env["dir"], site_dir(target)) + frag
    if target.startswith("assets/"):
        return rel(env["dir"], env["assets"](target)[0]) + frag
    return href


def build_md():
    md = MarkdownIt("commonmark", {"html": True, "highlight": highlight_code}).enable(["table", "strikethrough"])
    md.core.ruler.push("fx_transform", core_transform)
    rules = md.renderer.rules

    def render_html(tokens, idx, options, env):
        tok = tokens[idx]
        if tok.meta and tok.meta.get("trusted"):
            return tok.content
        tags = {t.lower() for t in re.findall(r"</?([a-zA-Z][a-zA-Z0-9]*)", tok.content)}
        return tok.content if tags <= ALLOWED_HTML else html.escape(tok.content)

    rules["html_block"] = render_html
    rules["html_inline"] = render_html

    def render_image(tokens, idx, options, env):
        tok = tokens[idx]
        alt = md.renderer.renderInlineAsText(tok.children or [], options, env)
        src = tok.attrGet("src") or ""
        if is_external(src):
            return f'<img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy">'
        site_path, w, h = env["assets"](resolve_md_target(env, src))
        dims = f' width="{w}" height="{h}"' if w else ""
        return (f'<img src="{html.escape(rel(env["dir"], site_path))}" alt="{html.escape(alt)}"{dims} '
                f'loading="lazy" decoding="async">')

    rules["image"] = render_image
    rules["table_open"] = lambda *a: '<div class="table-wrap"><table>\n'
    rules["table_close"] = lambda *a: "</table></div>\n"
    return md


def postprocess(body):
    # image + caption paragraphs -> <figure>
    body = re.sub(r"<p>(<img [^>]+>)</p>\s*<p><em>(.*?)</em></p>",
                  r'<figure class="figure">\1<figcaption>\2</figcaption></figure>', body, flags=re.S)
    body = re.sub(r"<p>(<img [^>]+>)</p>", r'<figure class="figure">\1</figure>', body)
    # heading anchors
    body = re.sub(r'(<h([2-4]) id="([^"]+)">)(.*?)(</h\2>)',
                  r'\1\4<a class="anchor" href="#\3" aria-label="Link to this section">#</a>\5', body, flags=re.S)
    return body


def card_grid(body):
    """GitBook card grids (a linked heading followed by a short description) -> card tiles."""
    body = re.sub(r'<h3 id="[^"]+"><a href="([^"]+)">(.*?)</a><a class="anchor"[^>]*>#</a></h3>\s*<p>(.*?)</p>',
                  r'<a class="card" href="\1"><span class="card-title">\2</span><span class="card-desc">\3</span></a>',
                  body, flags=re.S)
    return re.sub(r'((?:<a class="card".*?</a>\s*)+)', r'<div class="cards">\1</div>\n', body, flags=re.S)


# ------------------------------------------------------------------ templates
def nav_html(groups, cur_dir, active_href):
    active = None
    for g in groups:
        for n in walk(g["items"]):
            if n["href"] == active_href:
                active = n
    open_set = set()
    p = active
    while p is not None:
        open_set.add(id(p))
        p = p.get("parent")

    def item(n):
        ext = is_external(n["href"])
        href = n["href"] if ext else rel(cur_dir, site_dir(n["href"]))
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        cur = ' aria-current="page"' if n is active else ""
        title = html.escape(n["title"]) + (' <span class="ext" aria-hidden="true">↗</span>' if ext else "")
        if not n["children"]:
            return f'<li><a href="{html.escape(href)}"{attrs}{cur}>{title}</a></li>'
        is_open = id(n) in open_set
        kids = "".join(item(c) for c in n["children"])
        return (f'<li class="has-children{" open" if is_open else ""}"><div class="nav-row">'
                f'<a href="{html.escape(href)}"{attrs}{cur}>{title}</a>'
                f'<button class="nav-toggle" type="button" aria-expanded="{"true" if is_open else "false"}" '
                f'aria-label="Show pages in {html.escape(n["title"])}"><svg viewBox="0 0 24 24" aria-hidden="true">'
                f'<path d="M9 6l6 6-6 6"/></svg></button></div><ul>{kids}</ul></li>')

    parts = []
    for g in groups:
        label = f'<p class="nav-label">{html.escape(g["label"])}</p>' if g["label"] else ""
        parts.append(f'<div class="nav-group">{label}<ul>{"".join(item(n) for n in g["items"])}</ul></div>')
    about = rel(cur_dir, "about/")
    cur = ' aria-current="page"' if active_href == "__about__" else ""
    parts.append(f'<div class="nav-group nav-meta"><p class="nav-label">This archive</p><ul>'
                 f'<li><a href="{about}"{cur}>About this archive</a></li>'
                 f'<li><a href="{SNAPSHOT_URL}" target="_blank" rel="noopener">Wayback Machine snapshot '
                 f'<span class="ext" aria-hidden="true">↗</span></a></li></ul></div>')
    return "\n".join(parts)


def toc_html(headings):
    hs = [h for h in headings if 2 <= h[0] <= 4]
    if len(hs) < 2:
        return ""
    top = min(h[0] for h in hs)
    hs = [h for h in hs if h[0] <= top + 1]
    items = "".join(f'<li class="toc-l{lvl - top}"><a href="#{slug}">{html.escape(text)}</a></li>'
                    for lvl, slug, text in hs)
    return f'<p class="toc-label">On this page</p><ul>{items}</ul>'


FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
           "%3Crect width='32' height='32' rx='8' fill='%23111113'/%3E%3Cpath d='M10 9h12M10 16h12M10 23h7' "
           "stroke='%23fff' stroke-width='2.6' stroke-linecap='round'/%3E%3C/svg%3E")

ICON_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
ICON_SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
ICON_THEME = ('<svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>'
              '<svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/>'
              '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>')


def page_html(*, title, desc, body, nav, toc, crumbs, pager, provenance, root, page_dir):
    desc_html = f'<p class="lead">{desc}</p>' if desc else ""
    meta_desc = html.escape(re.sub(r"<[^>]+>", "", desc or f"{title} — archived fxhash documentation"))
    return f"""<!doctype html>
<html lang="en" data-root="{root}" data-page="{html.escape(page_dir)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · fxhash docs (archive)</title>
<meta name="description" content="{meta_desc}">
<meta property="og:title" content="{html.escape(title)} · fxhash docs (archive)">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="{root}assets/site.css">
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
<a class="skip-link" href="#content">Skip to content</a>
<div class="archive-bar"><p><strong>Archived copy</strong> of docs.fxhash.xyz, restored from the
<a href="{SNAPSHOT_URL}" target="_blank" rel="noopener">Wayback Machine snapshot of {SNAPSHOT_LABEL}</a>.
<span class="archive-extra">Preserved by <a href="{OWNER_URL}" target="_blank" rel="noopener">{OWNER_NAME}</a> ·
<a href="{root}about/">About this archive</a></span></p></div>
<header class="topbar">
  <button class="icon-btn menu-btn" type="button" aria-label="Open navigation" aria-controls="sidebar" aria-expanded="false">{ICON_MENU}</button>
  <a class="brand" href="{root or './'}"><span class="brand-name">{SITE_NAME}</span><span class="brand-tag">{SITE_TAG}</span></a>
  <div class="search" role="search">
    <span class="search-icon">{ICON_SEARCH}</span>
    <input id="search-input" type="search" placeholder="Search the docs" autocomplete="off" spellcheck="false"
      aria-label="Search the documentation" aria-controls="search-results" aria-expanded="false">
    <kbd class="search-key" aria-hidden="true">/</kbd>
    <div id="search-results" class="search-results" role="listbox" hidden></div>
  </div>
  <button class="icon-btn theme-btn" type="button" aria-label="Toggle dark mode">{ICON_THEME}</button>
</header>
<div class="layout">
  <nav id="sidebar" class="sidebar" aria-label="Documentation">{nav}</nav>
  <div class="scrim" hidden></div>
  <main id="content" class="main">
    {crumbs}
    <article class="doc">
      <header class="doc-head"><h1>{html.escape(title)}</h1>{desc_html}</header>
      {body}
    </article>
    {pager}
    {provenance}
  </main>
  <aside class="toc" aria-label="On this page">{toc}</aside>
</div>
<div class="lightbox" hidden><img alt=""></div>
<script src="{root}assets/site.js" defer></script>
</body>
</html>
"""


# ------------------------------------------------------------------ build
def main():
    groups = parse_summary()
    pages = [n for g in groups for n in walk(g["items"]) if not is_external(n["href"])]
    if os.path.exists(OUT):
        keep = os.path.join(OUT, "assets", "img")
        for entry in os.listdir(OUT):
            p = os.path.join(OUT, entry)
            if entry == "assets":
                for sub in os.listdir(p):
                    if os.path.join(p, sub) != keep:
                        sp = os.path.join(p, sub)
                        shutil.rmtree(sp) if os.path.isdir(sp) else os.remove(sp)
            else:
                shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)

    md = build_md()
    used_assets = {}

    def asset(target):
        name = target.split("/", 1)[1]
        if name not in used_assets:
            used_assets[name] = optimise_asset(name)
        return used_assets[name]

    index = []
    rendered = []
    for n in pages:
        meta, text = read_page(n["href"])
        d = site_dir(n["href"])
        env = {"md": n["href"], "dir": d, "ids": set(), "headings": [], "assets": asset}
        body = postprocess(md.render(text, env))
        if d == "":
            body = card_grid(body)
            env["headings"] = []  # its headings became cards
        rendered.append((n, meta, body, env, d))
        index.append({
            "t": meta.get("title", n["title"]), "u": d, "g": n["group"] or "",
            "h": [[t, s] for lvl, s, t in env["headings"] if lvl <= 4],
            "x": re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip(),
        })

    for i, (n, meta, body, env, d) in enumerate(rendered):
        root = rel(d, "") if d else ""
        root = "" if root == "./" else root
        title = meta.get("title", n["title"])
        desc = md.renderInline(meta["description"]) if meta.get("description") else ""
        # breadcrumbs
        trail, p = [], n.get("parent")
        while p is not None:
            trail.insert(0, f'<a href="{rel(d, site_dir(p["href"]))}">{html.escape(p["title"])}</a>')
            p = p.get("parent")
        if n["group"]:
            trail.insert(0, f"<span>{html.escape(n['group'])}</span>")
        crumbs = (f'<nav class="crumbs" aria-label="Breadcrumb">{" <span class=sep>/</span> ".join(trail)}</nav>'
                  if trail else "")
        # prev / next
        prev_n = rendered[i - 1][0] if i > 0 else None
        next_n = rendered[i + 1][0] if i + 1 < len(rendered) else None
        cards = []
        if prev_n:
            cards.append(f'<a class="pager-prev" href="{rel(d, site_dir(prev_n["href"]))}"><span>Previous</span>'
                         f'{html.escape(prev_n["title"])}</a>')
        if next_n:
            cards.append(f'<a class="pager-next" href="{rel(d, site_dir(next_n["href"]))}"><span>Next</span>'
                         f'{html.escape(next_n["title"])}</a>')
        pager = f'<nav class="pager" aria-label="Pagination">{"".join(cards)}</nav>'
        src = meta.get("source", "")
        prov = (f'<footer class="provenance"><p>Originally published at <a href="{html.escape(src)}" target="_blank" '
                f'rel="noopener">{html.escape(src.replace("https://", ""))}</a>. Restored from the '
                f'<a href="{html.escape(meta.get("archived", SNAPSHOT_URL))}" target="_blank" rel="noopener">'
                f'Wayback Machine capture of {html.escape(meta.get("captured", ""))}</a>.</p>'
                f'<p>Archive preserved by <a href="{OWNER_URL}" target="_blank" rel="noopener">{OWNER_NAME}</a>.</p></footer>')
        out = page_html(title=title, desc=desc, body=body, nav=nav_html(groups, d, n["href"]),
                        toc=toc_html(env["headings"]), crumbs=crumbs, pager=pager, provenance=prov,
                        root=root, page_dir=d)
        dest = os.path.join(OUT, d, "index.html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(out)

    # about page
    about_meta, about_text = {}, open(os.path.join(TOOLS, "about.md"), encoding="utf-8").read()
    h = re.match(r"\s*# (.+)\n", about_text)
    about_title = h.group(1).strip() if h else "About this archive"
    about_text = about_text[h.end():] if h else about_text
    env = {"md": "about.md", "dir": "about/", "ids": set(), "headings": [], "assets": asset}
    about_body = postprocess(md.render(about_text, env))
    out = page_html(title=about_title, desc="", body=about_body, nav=nav_html(groups, "about/", "__about__"),
                    toc=toc_html(env["headings"]), crumbs="", pager="", provenance="", root="../",
                    page_dir="about/")
    os.makedirs(os.path.join(OUT, "about"), exist_ok=True)
    open(os.path.join(OUT, "about", "index.html"), "w", encoding="utf-8").write(out)

    # static assets
    for f in os.listdir(TEMPLATE_DIR):
        shutil.copy2(os.path.join(TEMPLATE_DIR, f), os.path.join(OUT, "assets", f))
    css = open(os.path.join(OUT, "assets", "site.css"), encoding="utf-8").read()
    css += "\n/* syntax highlighting (generated by Pygments) */\n" + pygments_css()
    open(os.path.join(OUT, "assets", "site.css"), "w", encoding="utf-8").write(css)
    with open(os.path.join(OUT, "assets", "search-index.js"), "w", encoding="utf-8") as fh:
        fh.write("window.SEARCH_INDEX=" + json.dumps(index, ensure_ascii=False, separators=(",", ":")) + ";\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    # drop optimised images that are no longer referenced
    img_dir = os.path.join(OUT, "assets", "img")
    live = {os.path.basename(v[0]) for v in used_assets.values()}
    for f in os.listdir(img_dir) if os.path.isdir(img_dir) else []:
        if f not in live:
            os.remove(os.path.join(img_dir, f))
    json.dump(image_cache, open(CACHE, "w"))
    print(f"built {len(rendered) + 1} pages, {len(used_assets)} assets -> {os.path.relpath(OUT, ROOT)}/")


def pygments_css():
    light = HtmlFormatter(style="xcode").get_style_defs(".code")
    dark = HtmlFormatter(style="github-dark").get_style_defs(".code")

    def strip_bg(css):
        return "\n".join(l for l in css.splitlines()
                         if not re.match(r"^\.code \{|^pre \{|^td\.linenos|^span\.linenos|^\.code \.hll", l))

    light = strip_bg(light)
    dark = strip_bg(dark)
    dark_explicit = dark.replace(".code ", ':root[data-theme="dark"] .code ')
    dark_auto = dark.replace(".code ", ':root:not([data-theme="light"]) .code ')
    return f"{light}\n{dark_explicit}\n@media (prefers-color-scheme: dark) {{\n{dark_auto}\n}}\n"


if __name__ == "__main__":
    main()
