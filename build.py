#!/usr/bin/env python3
"""
Payments Ledger — static site generator.

Usage:   python3 build.py
Input:   content/modules.json   (the 12 course modules)
         content/articles/*.md  (your articles — see README.md for the format)
         content/site.json      (site name, URL, author)
Output:  dist/                  (upload this folder, or push it to GitHub Pages)
"""
import json, re, html, datetime, shutil, pathlib
import markdown

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"

site = json.loads((CONTENT / "site.json").read_text())
modules = json.loads((CONTENT / "modules.json").read_text())
BASE = site["url"].rstrip("/")
TODAY = datetime.date.today().isoformat()

def esc(s): return html.escape(str(s or ""))

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:80]

def md_to_html(text):
    return markdown.markdown(text, extensions=["tables", "fenced_code", "toc", "sane_lists"])

# ---------- articles ----------
def parse_article(path):
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")
        body = m.group(2)
    title = meta.get("title") or next((l.lstrip("# ").strip() for l in body.splitlines() if l.startswith("# ")), path.stem)
    body_wo_h1 = re.sub(r"^# .*\n", "", body, count=1) if not meta.get("title") else body
    date = meta.get("date") or datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()
    slug = meta.get("slug") or slugify(path.stem)
    tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
    summary = meta.get("summary") or re.sub(r"\s+", " ", re.sub(r"[#*`>\[\]()_]", "", body_wo_h1)).strip()[:180]
    words = len(body_wo_h1.split())
    return dict(title=title, date=date, slug=slug, tags=tags, module=meta.get("module", ""),
                summary=summary, html=md_to_html(body_wo_h1), words=words, draft=meta.get("draft","").lower()=="true")

articles = sorted(
    [a for a in (parse_article(p) for p in sorted((CONTENT / "articles").glob("*.md"))) if not a["draft"]],
    key=lambda a: a["date"], reverse=True)

# ---------- layout ----------
CSS = (ROOT / "style.css").read_text()

def page(title, body, desc, path, kind="website"):
    url = f"{BASE}/{path}".replace("/index.html", "/")
    depth = path.count("/")
    rel = "../"*depth if depth else "./"
    body = body.replace("{BASE}/", rel)
    ld = {"@context":"https://schema.org","@type":"Article" if kind=="article" else "WebPage",
          "headline":title,"description":desc,"url":url,"author":{"@type":"Person","name":site["author"]}}
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title) if title != site["name"] else esc(site["name"]) + " — " + esc(site["tagline"].split(" — ")[0])}{" · " + esc(site["name"]) if title != site["name"] else ""}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{esc(url)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{'article' if kind=='article' else 'website'}">
<meta property="og:url" content="{esc(url)}">
<meta name="twitter:card" content="summary">
<meta name="google-site-verification" content="PbGUo1pr13oBoi1uN125Hb_bBmVwdiA0v8xaJExeYZY" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Serif:wght@500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
<header class="top">
  <a class="brand" href="{rel}">{esc(site['name'])}</a>
  <nav>
    <a href="{rel}course/">Course</a>
    <a href="{rel}articles/">Articles</a>
    <a href="{rel}about/">About</a>
  </nav>
</header>
<main class="wrap">
{body}
</main>
<footer class="foot">
  <p>{esc(site['name'])} — notes on payments, Swift, ISO 20022 and the business-analyst craft, by {esc(site['author'])}. {esc(site.get('tagline',''))}</p>
  <p><a href="{rel}sitemap.xml">Sitemap</a> · <a href="{rel}feed.xml">RSS</a>{(' · <a href="'+esc(site['linkedin'])+'">LinkedIn</a>') if site.get('linkedin') else ''}</p>
</footer>
</body>
</html>"""

def write(path, content):
    p = DIST / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

# ---------- pages ----------
if DIST.exists(): shutil.rmtree(DIST)
DIST.mkdir()
urls = []

def kind_label(k): return {"text":"Read","video":"Watch","audio":"Listen","interactive":"Do"}.get(k,"Read")

def module_card(m, i):
    return f"""<a class="card" href="{{BASE}}/course/{m['id']}/">
  <span class="num">{i+1:02d}</span>
  <span class="ct"><strong>{esc(m['title'])}</strong><span class="sub">{esc(m['week'])} · {len(m['res'])} resources</span></span>
</a>"""

def article_row(a):
    tag = f'<span class="tag">{esc(a["module"])}</span> ' if a["module"] else ""
    return f"""<li><a href="{{BASE}}/articles/{a['slug']}/"><span class="at">{esc(a['title'])}</span>
  <span class="am">{tag}{esc(a['date'])} · {a['words']} words</span>
  <span class="as">{esc(a['summary'])}</span></a></li>"""

# Home
recent = "".join(article_row(a) for a in articles[:5]) or '<li class="empty">First articles coming soon.</li>'
home = f"""
<section class="hero">
  <h1>{esc(site['name'])}</h1>
  <p class="lede">{esc(site['tagline'])}</p>
  <p class="lede">A free, structured course on the payments domain — Indian rails, Swift and gpi, correspondent banking, MT and ISO 20022 messages, exceptions and investigations, payment hubs — plus the articles written along the way.</p>
  <p><a class="btn" href="{{BASE}}/course/">Start the course</a> <a class="btn ghost" href="{{BASE}}/articles/">Read the articles</a></p>
</section>
<h2>The course</h2>
<div class="grid">{"".join(module_card(m,i) for i,m in enumerate(modules))}</div>
<h2>Latest articles</h2>
<ul class="art-list">{recent}</ul>
"""
write("index.html", page(site["name"], home, site["tagline"], "index.html")); urls.append("")

# Course index
course = f"""
<h1>The course</h1>
<p class="lede">Twelve modules, about fourteen weeks at 6–8 hours a week. Every resource is free. Each module ends with an exercise and a checkpoint question — that's where the learning happens.</p>
<div class="grid">{"".join(module_card(m,i) for i,m in enumerate(modules))}</div>
<h2>Suggested schedule</h2>
<table><thead><tr><th>Week</th><th>Module</th></tr></thead><tbody>
{"".join(f"<tr><td>{esc(m['week'])}</td><td><a href='{{BASE}}/course/{m['id']}/'>{i+1:02d} · {esc(m['title'])}</a></td></tr>" for i,m in enumerate(modules))}
</tbody></table>
"""
write("course/index.html", page("The course", course, "A free 12-module course on payments, Swift, ISO 20022 and the business-analyst craft.", "course/index.html")); urls.append("course/")

# Module pages
for i, m in enumerate(modules):
    res = "".join(
        f"""<li><span class="kind {r['k']}">{kind_label(r['k'])}</span>
<span class="rt">{('<a href="'+esc(r['u'])+'" rel="noopener">'+esc(r['t'])+'</a>') if r.get('u') else esc(r['t'])}</span>
{('<div class="rn">'+esc(r['n'])+'</div>') if r.get('n') else ''}</li>""" for r in m["res"])
    related = [a for a in articles if a["module"] and (a["module"].lower().startswith(m["id"]) or a["module"].lower().startswith(f"{i+1:02d}"))]
    rel_html = f"<h2>Articles from this module</h2><ul class='art-list'>{''.join(article_row(a) for a in related)}</ul>" if related else ""
    prev = f'<a href="{{BASE}}/course/{modules[i-1]["id"]}/">← {esc(modules[i-1]["title"])}</a>' if i else "<span></span>"
    nxt = f'<a href="{{BASE}}/course/{modules[i+1]["id"]}/">{esc(modules[i+1]["title"])} →</a>' if i < len(modules)-1 else "<span></span>"
    body = f"""
<p class="crumb"><a href="{{BASE}}/course/">Course</a> · Module {i+1} of {len(modules)} · {esc(m['week'])}</p>
<h1>{esc(m['title'])}</h1>
<p class="lede">{esc(m['goal'])}</p>
<p class="small muted">{esc(m['topics'])}</p>
<h2>Resources</h2>
<ul class="res">{res}</ul>
<h2>Exercise</h2>
<div class="box"><p>{esc(m['ex'])}</p></div>
<h2>Checkpoint</h2>
<div class="box gold"><p>{esc(m['cp'])}</p></div>
{rel_html}
<div class="pager">{prev}{nxt}</div>
"""
    write(f"course/{m['id']}/index.html", page(f"{i+1:02d} · {m['title']}", body, m["goal"], f"course/{m['id']}/index.html")); urls.append(f"course/{m['id']}/")

# Articles index
alist = "".join(article_row(a) for a in articles) or '<li class="empty">No articles yet.</li>'
write("articles/index.html", page("Articles", f"<h1>Articles</h1><p class='lede'>Write-ups from the course: exercise answers, message explainers, comparison tables and the occasional opinion.</p><ul class='art-list'>{alist}</ul>",
      "Articles on payments, Swift, ISO 20022 and business analysis.", "articles/index.html")); urls.append("articles/")

# Article pages
for a in articles:
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in a["tags"])
    mod = next((m for i,m in enumerate(modules) if a["module"] and (a["module"].lower().startswith(m["id"]) or a["module"].lower().startswith(f"{i+1:02d}"))), None)
    modlink = f'<a href="{{BASE}}/course/{mod["id"]}/">{esc(mod["title"])}</a> · ' if mod else ""
    body = f"""
<p class="crumb"><a href="{{BASE}}/articles/">Articles</a></p>
<h1>{esc(a['title'])}</h1>
<p class="small muted">{modlink}{esc(a['date'])} · {a['words']} words {tags}</p>
<article class="prose">{a['html']}</article>
"""
    write(f"articles/{a['slug']}/index.html", page(a["title"], body, a["summary"], f"articles/{a['slug']}/index.html", kind="article")); urls.append(f"articles/{a['slug']}/")

# About
about_md = (CONTENT / "about.md").read_text() if (CONTENT / "about.md").exists() else f"# About\n\n{site['name']} is written by {site['author']}."
write("about/index.html", page("About", f"<article class='prose'>{md_to_html(about_md)}</article>", f"About {site['name']}", "about/index.html")); urls.append("about/")

# SEO files
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"  <url><loc>{BASE}/{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
write("feed.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>{esc(site['name'])}</title><link>{BASE}/</link><description>{esc(site['tagline'])}</description>
{"".join(f"<item><title>{esc(a['title'])}</title><link>{BASE}/articles/{a['slug']}/</link><pubDate>{a['date']}</pubDate><description>{esc(a['summary'])}</description></item>" for a in articles)}
</channel></rss>""")
write(".nojekyll", "")
write("404.html", page("Page not found", f"<h1>Page not found</h1><p class='lede'>Try the <a href='{{BASE}}/'>home page</a> or the <a href='{{BASE}}/course/'>course</a>.</p>", "Page not found", "404.html"))

print(f"Built {len(urls)} pages → {DIST}  ({len(articles)} articles)")
