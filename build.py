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
quizzes = json.loads((CONTENT / "quizzes.json").read_text()) if (CONTENT / "quizzes.json").exists() else {}
REPO = site.get("repo", "")
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
                series=meta.get("series", ""), order=int(meta.get("order", "0") or 0),
                summary=summary, html=md_to_html(body_wo_h1), words=words, draft=meta.get("draft","").lower()=="true")

articles = sorted(
    [a for a in (parse_article(p) for p in sorted((CONTENT / "articles").glob("*.md"))) if not a["draft"]],
    key=lambda a: (a["date"], -a["order"]), reverse=True)

SERIES_TITLES = site.get("series", {})
def series_parts(name):
    return sorted([x for x in articles if x["series"] == name], key=lambda x: x["order"])

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
<title>{esc(site["home_title"]) if title == site["name"] else esc(title) + " · " + esc(site["name"])}</title>
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
    <a href="{rel}feedback/">Feedback</a>
  </nav>
</header>
<main class="wrap">
{body}
</main>
<footer class="foot">
  <p>{esc(site['name'])} — {esc(site.get('tagline',''))} <a href="{rel}about/">About this site</a>.</p>
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
  <span class="ct"><strong>{esc(m['title'])}</strong><span class="sub">{esc(m['week'])} · {len(m['res'])} resources{' · quiz' if quizzes.get(m['id']) else ''}</span></span>
</a>"""

def article_row(a):
    tag = f'<span class="tag">{esc(a["module"])}</span> ' if a["module"] else ""
    return f"""<li><a href="{{BASE}}/articles/{a['slug']}/"><span class="at">{esc(a['title'])}</span>
  <span class="am">{tag}{esc(a['date'])} · {a['words']} words</span>
  <span class="as">{esc(a['summary'])}</span></a></li>"""

import urllib.parse as _up
def issue_link(kind, title):
    if not REPO: return "{BASE}/feedback/"
    labels = {"resource":"Suggest a resource", "error":"Report an error", "broken":"Broken link", "question":"Question"}
    t = _up.quote(f"[{labels.get(kind,kind)}] {title}")
    b = _up.quote(f"Page: {title}\n\n(Describe the resource, error or question here.)")
    return f"{REPO}/issues/new?title={t}&body={b}"
def feedback_box(title):
    return f"""<div class="feedback"><strong>Spotted an error or know a better resource?</strong>
<a href="{issue_link('error', title)}" rel="noopener">Report an error</a> ·
<a href="{issue_link('resource', title)}" rel="noopener">Suggest a resource</a> ·
<a href="{issue_link('broken', title)}" rel="noopener">Report a broken link</a> ·
<a href="{{BASE}}/feedback/">Other ways to get in touch</a></div>"""

def quiz_html(mid):
    qs = quizzes.get(mid)
    if not qs: return ""
    items = ""
    for qi, q in enumerate(qs):
        opts = "".join(f'<label class="opt"><input type="radio" name="q{qi}" value="{oi}"> <span>{esc(o)}</span></label>' for oi, o in enumerate(q["o"]))
        items += f'<fieldset class="qq" data-a="{q["a"]}"><legend>{qi+1}. {esc(q["q"])}</legend>{opts}<div class="why" hidden>{esc(q["x"])}</div></fieldset>'
    return f"""<h2 id="quiz">Quick quiz</h2>
<p class="small muted">Four questions. Nothing is recorded; it is just for you.</p>
<form class="quiz" onsubmit="return false">{items}
<div class="row"><button type="button" class="btn" data-check>Check my answers</button><button type="button" class="btn ghost" data-reset>Reset</button><span class="score" aria-live="polite"></span></div></form>
<script>
(function(){{var f=document.querySelector('form.quiz');if(!f)return;
f.querySelector('[data-check]').onclick=function(){{var n=0,t=0;f.querySelectorAll('.qq').forEach(function(q){{t++;var a=+q.dataset.a,c=q.querySelector('input:checked');q.classList.remove('right','wrong');q.querySelectorAll('.opt').forEach(function(l,i){{l.classList.toggle('is-answer',i===a);l.classList.toggle('is-wrong',!!c&&+c.value===i&&i!==a);}});if(c&&+c.value===a){{n++;q.classList.add('right');}}else if(c){{q.classList.add('wrong');}}q.querySelector('.why').hidden=!c;}});var s=f.querySelector('.score');s.textContent=n+' of '+t+' correct'+(n===t?' — well done.':n>=t/2?' — nearly there; read the explanations.':' — reread the module, then try again.');}};
f.querySelector('[data-reset]').onclick=function(){{f.reset();f.querySelectorAll('.qq').forEach(function(q){{q.classList.remove('right','wrong');q.querySelector('.why').hidden=true;q.querySelectorAll('.opt').forEach(function(l){{l.classList.remove('is-answer','is-wrong');}});}});f.querySelector('.score').textContent='';}};}})();
</script>"""

def series_teaser():
    out=""
    for key, stitle in SERIES_TITLES.items():
        parts=[x for x in series_parts(key) if x["order"]>0]; idx=next((x for x in series_parts(key) if x["order"]==0),None)
        if not parts: continue
        out+=f"""<div class="box"><p><strong>{esc(stitle)}</strong> — {len(parts)} parts that build the domain from first principles: instruments, push and pull, the four-corner model, clearing and settlement, accounting, cross-border, correspondent banking, Swift, SEPA and ISO 20022. Each part has worked examples and links to the next.</p>
<p style="margin-top:8px"><a class="btn" href="{{BASE}}/articles/{(idx or parts[0])['slug']}/">{'Read the series map' if idx else 'Start with part 1'}</a></p></div>"""
    return out

# Home
recent = "".join(article_row(a) for a in articles[:5]) or '<li class="empty">First articles coming soon.</li>'
home = f"""
<section class="hero">
  <h1>{esc(site['home_h1'])}</h1>
  <p class="lede">{esc(site['home_desc'])}</p>
  <p><a class="btn" href="{{BASE}}/course/">Start the course</a> <a class="btn ghost" href="{{BASE}}/articles/">Read the articles</a></p>
</section>
<h2>Start here: the series</h2>
{series_teaser()}
<h2>The course</h2>
<div class="grid">{"".join(module_card(m,i) for i,m in enumerate(modules))}</div>
<h2>Latest articles</h2>
<ul class="art-list">{recent}</ul>
"""
write("index.html", page(site["name"], home, site["home_desc"], "index.html")); urls.append("")

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
{quiz_html(m['id'])}
{rel_html}
{feedback_box(f"Module {i+1}: {m['title']}")}
<div class="pager">{prev}{nxt}</div>
"""
    write(f"course/{m['id']}/index.html", page(f"{i+1:02d} · {m['title']}", body, m["goal"], f"course/{m['id']}/index.html")); urls.append(f"course/{m['id']}/")

# Articles index
series_html = ""
for key, stitle in SERIES_TITLES.items():
    parts = series_parts(key)
    if parts:
        idx = next((x for x in parts if x["order"] == 0), None); numbered = [x for x in parts if x["order"] > 0]
        intro = f"<p class='lede small'>{len(numbered)} parts, written to be read in order." + (f" <a href='{{BASE}}/articles/{idx['slug']}/'>Start with the series map.</a>" if idx else "") + "</p>"
        series_html += f"<h2>{esc(stitle)}</h2>" + intro + "<ol class='series-list'>" + "".join(
            f'<li><a href="{{BASE}}/articles/{x["slug"]}/">{esc(x["title"])}</a><span class="as">{esc(x["summary"])}</span></li>' for x in numbered) + "</ol>"
others = [a for a in articles if not a["series"]]
alist = (series_html + ("<h2>Other articles</h2>" if series_html and others else "") +
         ("<ul class='art-list'>" + "".join(article_row(a) for a in others) + "</ul>" if others else "")) or '<li class="empty">No articles yet.</li>'
write("articles/index.html", page("Articles", f"<h1>Articles</h1><p class='lede'>Write-ups from the course: exercise answers, message explainers, comparison tables and the occasional opinion.</p>{alist}",
      "Articles on payments, Swift, ISO 20022 and business analysis.", "articles/index.html")); urls.append("articles/")

def series_nav(a):
    if not a["series"]: return ""
    allparts = series_parts(a["series"])
    index = next((x for x in allparts if x["order"] == 0), None)
    parts = [x for x in allparts if x["order"] > 0]
    if len(parts) < 2: return ""
    title = SERIES_TITLES.get(a["series"], a["series"])
    items = "".join(
        f'<li class="{"cur" if x["slug"]==a["slug"] else ""}">' +
        (esc(x["title"]) if x["slug"]==a["slug"] else f'<a href="{{BASE}}/articles/{x["slug"]}/">{esc(x["title"])}</a>') +
        "</li>" for x in parts)
    idx_link = f' · <a href="{{BASE}}/articles/{index["slug"]}/">Series map</a>' if index and index["slug"] != a["slug"] else ""
    if a["order"] == 0:
        head = f"{esc(title)} — all {len(parts)} parts"
        pager = ""
    else:
        i = next(k for k,x in enumerate(parts) if x["slug"] == a["slug"])
        head = f"{esc(title)} — part {i+1} of {len(parts)}{idx_link}"
        prev = f'<a href="{{BASE}}/articles/{parts[i-1]["slug"]}/">← Part {i}: {esc(parts[i-1]["title"])}</a>' if i>0 else (f'<a href="{{BASE}}/articles/{index["slug"]}/">← Series map</a>' if index else "<span></span>")
        nxt = f'<a href="{{BASE}}/articles/{parts[i+1]["slug"]}/">Part {i+2}: {esc(parts[i+1]["title"])} →</a>' if i<len(parts)-1 else "<span></span>"
        pager = f'<div class="pager">{prev}{nxt}</div>'
    return f"""{pager}
<aside class="series"><h3>{head}</h3><ol>{items}</ol></aside>"""

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
{series_nav(a)}
{feedback_box(a['title'])}
"""
    write(f"articles/{a['slug']}/index.html", page(a["title"], body, a["summary"], f"articles/{a['slug']}/index.html", kind="article")); urls.append(f"articles/{a['slug']}/")

# About
about_md = (CONTENT / "about.md").read_text() if (CONTENT / "about.md").exists() else f"# About\n\n{site['name']} is written by {site['author']}."
write("about/index.html", page("About", f"<article class='prose'>{md_to_html(about_md)}</article>", f"About {site['name']}", "about/index.html")); urls.append("about/")

# Feedback page
fb = f"""
<h1>Feedback</h1>
<p class="lede">This site improves when readers point out what is wrong, what is missing, or what explains something better. Three ways to do that.</p>
<h2>Report an error or suggest a resource</h2>
<p>Every module and article has links at the bottom that open a pre-filled form. You can also start from here:</p>
<p><a class="btn" href="{issue_link('error','General')}" rel="noopener">Report an error</a> <a class="btn ghost" href="{issue_link('resource','General')}" rel="noopener">Suggest a resource</a> <a class="btn ghost" href="{issue_link('question','General')}" rel="noopener">Ask a question</a></p>
<p class="small muted">These open on GitHub, where the site is hosted. You need a free GitHub account to post; it takes a minute to create and is worth having if you work anywhere near technology. Everything posted there is public, so don't include anything confidential.</p>
<h2>Reach me directly</h2>
<p>{('Message me on <a href="'+esc(site['linkedin'])+'" rel="noopener">LinkedIn</a>.') if site.get('linkedin') else 'A LinkedIn link will appear here shortly.'}</p>
<h2>What is most useful</h2>
<ul>
<li>A better free resource than one listed in a module, with a line on why.</li>
<li>A factual error, with a source.</li>
<li>A real-world example (anonymised) that would make an article clearer.</li>
<li>A question the site should answer and doesn't.</li>
</ul>
"""
write("feedback/index.html", page("Feedback", fb, "Report an error, suggest a resource or ask a question.", "feedback/index.html")); urls.append("feedback/")

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
