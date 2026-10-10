# Payments Domain Guide — your public website

A fast, Google-indexable static site: the 12-module course plus your articles. No database, no login, nothing to maintain — just files.

```
site-src/
├── build.py            ← generates the site
├── style.css
├── content/
│   ├── site.json       ← site name, your URL, author, LinkedIn  ← EDIT THIS FIRST
│   ├── about.md        ← the About page
│   ├── modules.json    ← the 12 course modules
│   └── articles/       ← one .md file per article  ← ADD ARTICLES HERE
└── dist/               ← the built site (this is what gets published)
```

## Put it online in 10 minutes (free, on GitHub Pages)

1. **Create a GitHub account** at github.com if you don't have one. Pick a username — it becomes part of your web address.
2. **Create a new repository** called `payments-domain-guide`, set to Public. Don't add a README.
3. **Edit `content/site.json`**: set `"url"` to `https://sushmitabuksh.github.io/payments-domain-guide` (your real username), and add your LinkedIn URL.
4. **Build** on your computer (needs Python 3):
   ```
   pip install markdown
   python3 build.py
   ```
5. **Upload the whole `site-src` folder** to the repository (drag and drop on github.com → "Add file → Upload files" → commit).
6. In the repository: **Settings → Pages → Build and deployment → Source: "GitHub Actions"**. The included workflow (`.github/workflows/pages.yml`) builds and publishes automatically on every upload. First run takes about a minute.
7. Your site is live at `https://sushmitabuksh.github.io/payments-domain-guide/`.

**Prefer not to use GitHub?** Drag the `dist` folder onto app.netlify.com/drop — you get a public URL instantly. You'll re-drag it each time you add an article.

**Want your own domain** (e.g. `paymentsledger.in`)? Buy one from any registrar (~₹800/year), then in GitHub Settings → Pages → Custom domain, follow the prompts. Update `"url"` in site.json to match.

## Getting onto Google

GitHub Pages sites are public and crawlable, but Google won't know yours exists until you tell it:

1. Go to **search.google.com/search-console**, add your site URL, verify ownership (the "HTML tag" method: paste the tag they give you into `build.py` inside `<head>` — ask me and I'll add it).
2. **Sitemaps → submit** `https://sushmitabuksh.github.io/payments-domain-guide/sitemap.xml`.
3. First indexing takes a few days to a couple of weeks. Each time you add an article, the sitemap updates automatically; Google re-crawls on its own, or you can request indexing of the new page in Search Console.
4. **Share each article on LinkedIn** with the link. Inbound links are the strongest signal that the page is worth ranking.

Realistic expectation: a new site with 2 articles won't rank for "ISO 20022" — the big players own that. It *will* rank for specific long-tail questions ("MT942 vs MT940 difference", "camt.056 vs camt.029") once you have an article that answers them well. Write for those.

## Adding an article

Create a file in `content/articles/`, named `YYYY-MM-DD-short-title.md`:

```markdown
---
title: MT940 vs MT942 — what the difference actually is
date: 2026-10-21
module: 07 MT messages
tags: swift, mt940, mt942, statements
summary: One is the end-of-day statement, the other is an intraday report. Here's how to tell them apart and why it matters for reconciliation.
---

Your article in Markdown. Headings with ##, lists with -, tables with |, code with ```.
Link to a module like this: [module 7](../../course/m7/)
```

- `module` can be `01 Intro` … `12 BA add-ons` or `General`; it links the article to its module page.
- `draft: true` in the front matter hides an article until you're ready.
- Then run `python3 build.py` and upload (or just upload the .md file to GitHub — the workflow rebuilds for you).

**Easier route:** paste your draft to me in Claude and say "add this as an article" — I'll write the file, build, and hand you the updated folder.

## Changing the course

`content/modules.json` holds every module: title, goal, resources, exercise, checkpoint. Edit it (or ask me to), rebuild, upload.
