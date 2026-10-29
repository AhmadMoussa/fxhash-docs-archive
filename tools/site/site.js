/* fxhash docs archive — site behaviour (no dependencies) */
(function () {
  "use strict";
  var doc = document.documentElement;
  var root = doc.getAttribute("data-root") || "";
  var isFile = location.protocol === "file:";

  function store(key, value) { try { localStorage.setItem(key, value); } catch (e) { /* storage unavailable */ } }

  // Opened straight from disk, directory links need an explicit index.html.
  function fixHref(href) {
    if (!isFile || !href || /^[a-z]+:|^#|^\/\//i.test(href)) return href;
    var parts = href.split("#");
    var path = parts[0];
    if (path === "" ) return href;
    if (/\/$/.test(path) || path === "." || path === "..") path = path.replace(/\/?$/, "/") + "index.html";
    return path + (parts.length > 1 ? "#" + parts.slice(1).join("#") : "");
  }
  if (isFile) {
    document.querySelectorAll("a[href]").forEach(function (a) { a.setAttribute("href", fixHref(a.getAttribute("href"))); });
  }

  // ------------------------------------------------------------ theme
  var themeBtn = document.querySelector(".theme-btn");
  function currentTheme() {
    return doc.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var next = currentTheme() === "dark" ? "light" : "dark";
    doc.dataset.theme = next;
    store("theme", next);
  });

  // ------------------------------------------------------------ mobile navigation
  var menuBtn = document.querySelector(".menu-btn");
  var scrim = document.querySelector(".scrim");
  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    if (menuBtn) menuBtn.setAttribute("aria-expanded", String(open));
    if (scrim) scrim.hidden = !open;
  }
  if (menuBtn) menuBtn.addEventListener("click", function () { setNav(!document.body.classList.contains("nav-open")); });
  if (scrim) scrim.addEventListener("click", function () { setNav(false); });

  document.querySelectorAll(".nav-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.closest("li");
      var open = !li.classList.contains("open");
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
  });
  var current = document.querySelector('.sidebar a[aria-current="page"]');
  if (current) {
    var sb = document.querySelector(".sidebar");
    var top = current.offsetTop - sb.clientHeight / 3;
    if (top > 0) sb.scrollTop = top;
  }

  // ------------------------------------------------------------ code blocks
  document.querySelectorAll(".doc pre.code").forEach(function (pre) {
    var wrap = document.createElement("div");
    wrap.className = "codeblock";
    var bar = document.createElement("div");
    bar.className = "codeblock-bar";
    var lang = document.createElement("span");
    lang.className = "codeblock-lang";
    lang.textContent = pre.getAttribute("data-lang") || "";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", function () {
      var text = pre.innerText;
      var done = function () { btn.textContent = "Copied"; setTimeout(function () { btn.textContent = "Copy"; }, 1400); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () {});
      else {
        var ta = document.createElement("textarea");
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) { /* ignore */ }
        ta.remove();
      }
    });
    bar.appendChild(lang);
    bar.appendChild(btn);
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(bar);
    wrap.appendChild(pre);
  });

  // ------------------------------------------------------------ "On this page" highlighting
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var targets = tocLinks.map(function (a) { return document.getElementById(decodeURIComponent(a.hash.slice(1))); });
    var visible = new Set();
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) visible.add(e.target); else visible.delete(e.target); });
      var idx = -1;
      targets.forEach(function (t, i) { if (t && visible.has(t) && idx === -1) idx = i; });
      if (idx === -1) {
        targets.forEach(function (t, i) { if (t && t.getBoundingClientRect().top < 120) idx = i; });
      }
      tocLinks.forEach(function (a, i) { a.classList.toggle("active", i === idx); });
    }, { rootMargin: "-70px 0px -65% 0px" });
    targets.forEach(function (t) { if (t) obs.observe(t); });
  }

  // ------------------------------------------------------------ image zoom
  var lightbox = document.querySelector(".lightbox");
  if (lightbox) {
    var lbImg = lightbox.querySelector("img");
    document.querySelectorAll(".doc .figure img").forEach(function (img) {
      img.addEventListener("click", function () {
        lbImg.src = img.currentSrc || img.src;
        lbImg.alt = img.alt;
        lightbox.hidden = false;
      });
    });
    lightbox.addEventListener("click", function () { lightbox.hidden = true; lbImg.removeAttribute("src"); });
  }

  // ------------------------------------------------------------ search
  var input = document.getElementById("search-input");
  var results = document.getElementById("search-results");
  var index = null, loading = false, selected = -1, pendingQuery = null;

  function loadIndex() {
    if (index || loading) return;
    loading = true;
    var s = document.createElement("script");
    s.src = root + "assets/search-index.js";
    s.onload = function () { index = window.SEARCH_INDEX || []; if (pendingQuery !== null) run(pendingQuery); };
    document.head.appendChild(s);
  }

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function highlight(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) {
      out = out.replace(new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi"), "<mark>$1</mark>");
    });
    return out;
  }
  function snippet(text, terms) {
    var lower = text.toLowerCase(), pos = -1;
    for (var i = 0; i < terms.length && pos < 0; i++) pos = lower.indexOf(terms[i]);
    if (pos < 0) return text.slice(0, 140) + (text.length > 140 ? "…" : "");
    var start = Math.max(0, pos - 60), end = Math.min(text.length, pos + 110);
    return (start > 0 ? "…" : "") + text.slice(start, end) + (end < text.length ? "…" : "");
  }

  function run(q) {
    pendingQuery = q;
    if (!index) { loadIndex(); return; }
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { close(); return; }
    var scored = [];
    index.forEach(function (p) {
      var title = p.t.toLowerCase(), text = p.x.toLowerCase(), score = 0, heading = null, ok = true;
      terms.forEach(function (t) {
        var inTitle = title.indexOf(t) >= 0, inText = text.indexOf(t) >= 0, inHead = false;
        p.h.forEach(function (h) {
          if (h[0].toLowerCase().indexOf(t) >= 0) { inHead = true; if (!heading && !inTitle) heading = h; }
        });
        if (!inTitle && !inText && !inHead) ok = false;
        if (inTitle) score += title.indexOf(t) === 0 ? 14 : 10;
        if (inHead) score += 5;
        if (inText) score += Math.min(6, text.split(t).length - 1);
      });
      if (ok) scored.push({ p: p, score: score, heading: heading });
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    render(scored.slice(0, 12), terms);
  }

  function render(list, terms) {
    selected = -1;
    if (!list.length) {
      results.innerHTML = '<div class="sr-empty">No results for “' + esc(input.value) + '”</div>';
    } else {
      results.innerHTML = list.map(function (r, i) {
        var url = root + r.p.u + (r.heading ? "#" + r.heading[1] : "");
        return '<a role="option" id="sr-' + i + '" href="' + esc(fixHref(url || "./")) + '">' +
          (r.p.g ? '<span class="sr-group">' + esc(r.p.g) + "</span>" : "") +
          '<span class="sr-title">' + highlight(r.p.t, terms) +
          (r.heading ? ' <span class="sr-heading">› ' + highlight(r.heading[0], terms) + "</span>" : "") + "</span>" +
          '<span class="sr-snippet">' + highlight(snippet(r.p.x, terms), terms) + "</span></a>";
      }).join("");
    }
    results.hidden = false;
    input.setAttribute("aria-expanded", "true");
  }
  function close() {
    results.hidden = true;
    input.setAttribute("aria-expanded", "false");
    selected = -1;
  }
  function move(delta) {
    var items = results.querySelectorAll("a");
    if (!items.length) return;
    selected = (selected + delta + items.length) % items.length;
    items.forEach(function (a, i) { a.setAttribute("aria-selected", String(i === selected)); });
    items[selected].scrollIntoView({ block: "nearest" });
    input.setAttribute("aria-activedescendant", items[selected].id);
  }

  if (input && results) {
    input.addEventListener("focus", loadIndex);
    input.addEventListener("input", function () { run(input.value.trim()); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Enter") {
        var items = results.querySelectorAll("a");
        var target = items[selected >= 0 ? selected : 0];
        if (target) { e.preventDefault(); location.href = target.href; }
      } else if (e.key === "Escape") { close(); input.blur(); }
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".search")) close(); });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && input && document.activeElement !== input && !/input|textarea|select/i.test(document.activeElement.tagName)) {
      e.preventDefault();
      input.focus();
    }
    if (e.key === "Escape") {
      setNav(false);
      if (lightbox && !lightbox.hidden) lightbox.click();
    }
  });
})();
