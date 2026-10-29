# fxhash Documentation — Archived Copy

A recovered copy of the fxhash documentation site (**docs.fxhash.xyz**), rebuilt from the Internet Archive's Wayback Machine snapshot of **13 March 2026**:
<https://web.archive.org/web/20260313230640/https://docs.fxhash.xyz/>

The repository contains the documentation in two forms: a browsable static **website** and the plain **Markdown** it is built from.

| Folder | What's inside |
| --- | --- |
| [`docs/`](docs/) | The website: 71 documentation pages plus an About page, with search, light/dark themes and a mobile layout. Plain HTML/CSS/JS with no build step needed on the server. |
| [`markdown/`](markdown/README.md) | All 71 pages as Markdown in GitBook's folder layout, with a [`SUMMARY.md`](markdown/SUMMARY.md) table of contents and full-resolution images in `markdown/assets/`. |
| `archived-source/` | The raw Wayback Machine captures each page was converted from, plus `manifest.json` linking each file to its capture. |
| `tools/` | `build_site.py`, which regenerates `docs/` from `markdown/`, plus the site's stylesheet, script and About page text. |

## Publishing on GitHub Pages

1. Create a new repository on GitHub, then push this folder to it:

   ```bash
   git init && git add . && git commit -m "fxhash documentation archive"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

2. In the repository, open **Settings → Pages**. Under *Build and deployment*, choose **Deploy from a branch**, then select the **`main`** branch and the **`/docs`** folder, and save.
3. After a minute or so the site is live at `https://<your-username>.github.io/<repo-name>/`.

All links are relative, so the site works at that sub-path, on a custom domain, or on any other static host. To use a custom domain (for example a subdomain of your blog), add it under **Settings → Pages → Custom domain** and create the DNS record GitHub asks for.

## Linking it from your blog

- **As a link:** add the Pages URL to your blog's navigation, or to a portfolio or "Other pages" page.
- **Embedded:** in a Ghost HTML card (or any HTML block) you can frame the whole site:

  ```html
  <iframe src="https://<your-username>.github.io/<repo-name>/" style="width:100%;height:85vh;border:0;border-radius:12px" loading="lazy" title="fxhash documentation archive"></iframe>
  ```

## Rebuilding the site

You only need this if you change something: page content in `markdown/`, the About page in `tools/about.md`, or the settings at the top of `tools/build_site.py` (site name, your name and link, banner text).

```bash
pip install -r tools/requirements.txt
```

```bash
python3 tools/build_site.py
```

To preview locally, serve the `docs/` folder and open <http://localhost:8642>:

```bash
python3 -m http.server 8642 --directory docs
```

The sidebar follows `markdown/SUMMARY.md`. To remove a page from the site, delete its line there and rebuild.

## Notes on the conversion

- **Provenance.** Each Markdown page starts with front matter giving its original URL, the exact Wayback capture it came from, and the capture date. Each web page shows the same in its footer. 65 pages come from captures on 10–13 March 2026. The *Collector's Code of Conduct* comes from 17 February 2026, the closest capture available. Five pages come from 11 April 2026, where the archive stored GitBook's Markdown source rather than the rendered page: *Reserves & Allow Lists*, *IPFS*, *ONCHFS* (Knowledge Base), *Adding Funds to Your Wallet* and *Artists' Code of Conduct*.
- **Formatting.** GitBook callouts become GitHub-style alerts in the Markdown (`> [!NOTE]`, `> [!WARNING]`, …) and coloured callout boxes on the website. Tabs are shown as bold labels, expandable blocks as `<details>`, and stepper steps as numbered headings. Code blocks keep their language wherever GitBook recorded one.
- **Embeds.** CodePen demos and the YouTube video are embedded live on the website and appear as links in the Markdown. The one embedded screen recording was downloaded to the assets folder.
- **Images** were recovered at full resolution from GitBook's file storage, with the Wayback Machine as a fallback. The website uses resized WebP copies, about 13 MB in total instead of 108 MB. Two small interface screenshots on *Minting Interface Walkthrough* were never archived and are marked as missing.
- **Kept as published.** A few formatting artifacts from the original site, such as escaped `\*\*` markers and a stray `<aside>` left over from a Notion import, are reproduced exactly as they appeared on the live site.
