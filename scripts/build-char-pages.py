#!/usr/bin/env python3
"""
Generate the static SEO pages for the character explorer.

Reads learn/char-data.js (built by build-char-data.py) and writes:

  learn/characters/<slug>.html   one crawlable reference page per character:
                                 full glyph SVG, stroke-order strip, pinyin,
                                 meaning, radical, origin story, common word
                                 and example sentence (with audio), plus a
                                 deep link into the interactive explorer.
  learn/characters/index.html    the browsable/crawlable index of all 300,
                                 grouped by theme.
  sitemap.xml                    regenerated with every page.

Run AFTER build-char-data.py whenever the character set changes:

    python3 scripts/build-char-data.py
    python3 scripts/build-char-pages.py

The pages are plain HTML with no JavaScript apart from analytics — the point
is that search engines (and AI assistants) can read all 300 characters'
content, which the JS-rendered explorer alone does not expose.
"""
import datetime
import html
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

OUT_DIR = os.path.join("learn", "characters")
SITE = "https://caseychinese.org"
TODAY = datetime.date.today().isoformat()

GROUP_ZH = {
    "Me & my body": "我和我的身体", "Family & people": "家人和人们",
    "Numbers & counting": "数字和数数", "Nature & weather": "自然和天气",
    "Animals": "动物", "Food & drink": "吃的喝的",
    "Colours & describing": "颜色和形容", "Everyday actions": "每天做的事",
    "School & learning": "学校和学习", "Out & about": "出门走走",
    "Time & days": "时间和日子", "Position & direction": "位置和方向",
    "Come & go": "来来去去", "Think & feel": "想和感觉",
    "Question words": "问问题", "Little glue words": "小小连接词",
    "Can & must": "能与要", "This & that": "这个那个",
    "Songs, games & stories": "唱歌游戏讲故事",
}


def load_data():
    src = open("learn/char-data.js", encoding="utf-8").read()
    m = re.search(r"window\.CHAR_DATA = (\[.*\]);", src, re.S)
    if not m:
        sys.exit("could not find CHAR_DATA in learn/char-data.js")
    return json.loads(m.group(1))


def ascii_pinyin(py):
    """rén -> ren (tone marks stripped, ü -> u)."""
    s = unicodedata.normalize("NFD", py)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def slugify(d, used):
    base = ascii_pinyin(d["py"]) + "-" + re.sub(r"[^a-z0-9]+", "-", d["en"].lower()).strip("-")
    base = base[:48].rstrip("-")
    slug, n = base, 1
    while slug in used:
        n += 1
        slug = f"{base}-{n}"
    used.add(slug)
    return slug


def esc(s):
    return html.escape(s, quote=True)


def ruby(seg, lang_wrap=True):
    """[["大","dà"],["，",""]] -> ruby markup, one ruby per character."""
    parts = []
    for ch, py in seg:
        if py:
            parts.append(f"<ruby>{esc(ch)}<rt>{esc(py)}</rt></ruby>")
        else:
            parts.append(f"<span class=\"punct\">{esc(ch)}</span>")
    inner = "".join(parts)
    return f'<span lang="zh-Hans">{inner}</span>' if lang_wrap else inner


def seg_text(seg):
    return "".join(p[0] for p in seg)


def glyph_svg(d, cls="glyph"):
    """Full character, all strokes filled, on the practice grid."""
    paths = "".join(f'<path d="{p}"/>' for p in d["s"])
    return (
        f'<svg class="{cls}" viewBox="0 0 1024 1024" role="img" '
        f'aria-label="The character {esc(d["ch"])} written in full">'
        '<rect x="3" y="3" width="1018" height="1018" rx="10" class="g-frame"/>'
        '<line class="g-dash" x1="512" y1="14" x2="512" y2="1010"/>'
        '<line class="g-dash" x1="14" y1="512" x2="1010" y2="512"/>'
        '<line class="g-diag" x1="40" y1="40" x2="984" y2="984"/>'
        '<line class="g-diag" x1="984" y1="40" x2="40" y2="984"/>'
        f'<g class="ink" transform="translate(0,900) scale(1,-1)">{paths}</g></svg>'
    )


def stroke_strip(d):
    """One small frame per stroke: strokes 1..i shown, stroke i highlighted.
    Paths are defined once and reused with <use> to keep pages small."""
    n = len(d["s"])
    defs = "".join(f'<path id="s{i}" d="{p}"/>' for i, p in enumerate(d["s"]))
    frames = []
    for i in range(n):
        done = "".join(f'<use href="#s{j}"/>' for j in range(i))
        frames.append(
            f'<svg class="frame" viewBox="0 0 1024 1024" role="img" '
            f'aria-label="Stroke {i + 1} of {n}">'
            f'<g transform="translate(0,900) scale(1,-1)">'
            f'<g class="done">{done}</g><g class="now"><use href="#s{i}"/></g>'
            f"</g></svg>"
        )
    return (
        f'<svg class="frame-defs" aria-hidden="true"><defs>{defs}</defs></svg>'
        + "".join(frames)
    )


CSP = (
    "default-src 'self'; script-src 'self' https://*.googletagmanager.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com; "
    "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com "
    "https://*.googletagmanager.com https://stats.g.doubleclick.net; "
    "object-src 'none'; base-uri 'self'; form-action 'self' mailto:; "
    "upgrade-insecure-requests"
)

STYLE = """
:root{--red:#F08379;--red-deep:#C84B3F;--red-tint:#FCE6E2;--bg:#FFF8F5;--bg-warm:#FBEFE9;
--paper:#FFFFFF;--ink:#26201E;--ink-soft:#5C504B;--ink-mute:#8E7F79;--line:#EFDDD5;
--ghost:#EFE2DC;--sans:'Manrope',system-ui,-apple-system,sans-serif;
--serif:'Newsreader','Times New Roman',serif;--zh:'Noto Serif SC','Songti SC',serif;}
*{box-sizing:border-box;}
body{margin:0;font-family:var(--sans);color:var(--ink);background:var(--bg);
font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;}
a{color:inherit;}
.wrap{max-width:880px;margin:0 auto;padding:0 24px;}
.nav{position:sticky;top:0;z-index:5;background:rgba(255,248,245,.92);backdrop-filter:blur(8px);
border-bottom:1px solid var(--line);}
.nav-inner{display:flex;align-items:center;justify-content:space-between;gap:16px;height:56px;}
.nav a{text-decoration:none;font-size:13.5px;font-weight:600;white-space:nowrap;}
.nav .links{display:flex;gap:18px;}
.nav .links a:hover{color:var(--red-deep);}
.crumbs{font-size:12.5px;color:var(--ink-mute);margin:22px 0 0;}
.crumbs a{color:var(--ink-mute);}
.crumbs a:hover{color:var(--red-deep);}
h1{font-family:var(--serif);font-weight:400;font-size:clamp(28px,4.5vw,40px);
letter-spacing:-.01em;margin:14px 0 4px;}
h1 .zh{font-family:var(--zh);font-weight:600;color:var(--red-deep);}
h1 .py{color:var(--ink-soft);font-size:.72em;}
.sub{color:var(--ink-soft);margin:0 0 26px;max-width:640px;}
h2{font-family:var(--serif);font-weight:400;font-size:clamp(20px,2.6vw,26px);margin:42px 0 12px;}
h2 .zh{font-family:var(--zh);font-size:.72em;color:var(--ink-mute);margin-left:10px;}
.card{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:26px;}
.hero-grid{display:grid;grid-template-columns:minmax(200px,260px) 1fr;gap:30px;align-items:start;}
@media(max-width:640px){.hero-grid{grid-template-columns:1fr;}}
.glyph{width:100%;height:auto;display:block;}
.g-frame{fill:#fff;stroke:var(--line);stroke-width:3;}
.g-dash,.g-diag{stroke:var(--ghost);stroke-width:3;stroke-dasharray:14 16;fill:none;}
.ink path{fill:var(--red-deep);}
.facts{display:grid;gap:12px;font-size:15.5px;}
.facts .lbl{text-transform:uppercase;letter-spacing:.14em;font-size:10.5px;font-weight:700;
color:var(--ink-mute);display:block;}
.facts .zh-big{font-family:var(--zh);font-size:19px;color:var(--red-deep);}
.strip{display:flex;flex-wrap:wrap;gap:8px;}
.frame-defs{position:absolute;width:0;height:0;overflow:hidden;}
.frame{width:64px;height:64px;background:#fff;border:1px solid var(--line);border-radius:10px;}
.frame .done use{fill:var(--ghost);}
.frame .now use{fill:var(--red-deep);}
.say-row{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin-top:10px;}
audio{height:36px;max-width:100%;}
.zh-line{font-family:var(--zh);font-size:clamp(22px,3.2vw,28px);line-height:2.1;color:var(--ink);}
.zh-line rt{font-family:var(--sans);font-size:11px;font-weight:600;color:var(--ink-soft);}
.zh-line .punct{opacity:.5;}
.mean{color:var(--ink-soft);font-style:italic;font-family:var(--serif);margin:6px 0 0;}
.origin{font-family:var(--serif);font-size:18.5px;color:var(--ink-soft);max-width:640px;margin:0;}
.cta{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;font-weight:600;
font-size:14.5px;padding:12px 22px;border-radius:999px;margin-top:8px;}
.cta:hover{background:var(--red-deep);}
.pn{display:flex;justify-content:space-between;gap:14px;margin:44px 0 0;font-size:14.5px;}
.pn a{text-decoration:none;font-weight:600;color:var(--ink-soft);border:1px solid var(--line);
border-radius:999px;padding:9px 18px;background:var(--paper);}
.pn a:hover{color:var(--red-deep);border-color:var(--red);}
.pn .zh{font-family:var(--zh);color:var(--red-deep);}
.foot{border-top:1px solid var(--line);margin-top:56px;padding:26px 0 40px;font-size:13px;
color:var(--ink-mute);display:flex;flex-wrap:wrap;gap:10px 26px;justify-content:space-between;}
.foot a{color:var(--ink-mute);}
.foot a:hover{color:var(--red-deep);}
/* index page */
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 6px;font-size:13px;}
.toc a{text-decoration:none;border:1px solid var(--line);background:var(--paper);
border-radius:999px;padding:6px 13px;font-weight:600;color:var(--ink-soft);}
.toc a:hover{color:var(--red-deep);border-color:var(--red);}
.char-list{list-style:none;margin:14px 0 0;padding:0;display:grid;
grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px;}
.char-list a{display:flex;align-items:baseline;gap:10px;text-decoration:none;background:var(--paper);
border:1px solid var(--line);border-radius:12px;padding:10px 14px;font-size:14.5px;}
.char-list a:hover{border-color:var(--red);}
.char-list .zh{font-family:var(--zh);font-size:24px;color:var(--red-deep);line-height:1.2;}
.char-list .py{font-weight:700;}
.char-list .en{color:var(--ink-mute);}
"""


def head(title, desc, canonical_path, og_title=None, extra=""):
    return f"""<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="referrer" content="strict-origin-when-cross-origin" />
<meta http-equiv="Content-Security-Policy" content="{CSP}" />
<meta name="robots" content="index, follow" />
<meta name="theme-color" content="#F08379" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{SITE}{canonical_path}" />
<meta property="og:type" content="article" />
<meta property="og:site_name" content="Casey Foundation Chinese School" />
<meta property="og:locale" content="en_AU" />
<meta property="og:title" content="{esc(og_title or title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{SITE}{canonical_path}" />
<meta property="og:image" content="{SITE}/images/og-characters.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" type="image/png" href="../../favicon.png" />
<link rel="apple-touch-icon" href="../../apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&family=Newsreader:ital,wght@0,400;1,400&family=Noto+Serif+SC:wght@400;500;600&display=swap" rel="stylesheet" />
{extra}<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TLRWEHJX8P"></script>
<script src="../../js/gtag-init.js"></script>
<style>{STYLE}</style>"""


def nav_html():
    return """<nav class="nav" aria-label="Site">
  <div class="wrap nav-inner">
    <a href="../../index.html">Casey Foundation Chinese School · <span lang="zh-Hans">Casey 中文学校</span></a>
    <div class="links">
      <a href="index.html">All 300 characters</a>
      <a href="../../characters.html">Interactive explorer</a>
    </div>
  </div>
</nav>"""


def footer_html():
    return """<footer class="foot">
  <div class="wrap" style="display:contents">
    <div>© Casey Foundation Chinese School · <span lang="zh-Hans">Casey 中文学校</span> — Saturday Chinese classes in Narre Warren, Victoria</div>
    <div><a href="../../index.html">Home</a> · <a href="../../characters.html">Interactive explorer</a> · <a href="index.html">All characters</a> · <a href="../../index.html#contact">Contact</a></div>
  </div>
</footer>"""


def breadcrumb_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u}
            for i, (n, u) in enumerate(items)
        ],
    }


def ld_script(obj):
    return ('<script type="application/ld+json">\n'
            + json.dumps(obj, ensure_ascii=False, indent=1)
            + "\n</script>\n")


def char_page(d, i, slug, prev_link, next_link):
    ch, py, en = d["ch"], d["py"], d["en"]
    n = len(d["s"])
    word_zh, word_en = seg_text(d["word"]["seg"]), d["word"]["en"]
    ex_zh, ex_en = seg_text(d["ex"]["seg"]), d["ex"]["en"]
    path = f"/learn/characters/{slug}.html"
    stroke_word = "stroke" if n == 1 else "strokes"

    title = f'{ch} ({py}) — Chinese Character for “{en}”: Stroke Order, Meaning & Examples'
    desc = (f"Learn the Chinese character {ch} ({py}, “{en}”): stroke order ({n} {stroke_word}), "
            f"Mandarin pronunciation audio, origin, the word {word_zh} ({word_en}) "
            f"and an example sentence. Free from Casey Foundation Chinese School.")

    ld = {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": f"Chinese character {ch} ({py}) — {en}",
        "description": desc,
        "url": SITE + path,
        "inLanguage": ["en", "zh-Hans"],
        "isAccessibleForFree": True,
        "learningResourceType": "Reference",
        "educationalLevel": "Beginner",
        "teaches": f"How to write and pronounce the Chinese character {ch} ({py}, {en})",
        "isPartOf": {
            "@type": "Collection",
            "name": "300 Chinese Characters for Beginners",
            "url": f"{SITE}/learn/characters/",
        },
        "provider": {
            "@type": "EducationalOrganization",
            "@id": f"{SITE}/#school",
            "name": "Casey Foundation Chinese School",
            "url": SITE,
        },
    }
    crumbs = breadcrumb_ld([
        ("Casey Foundation Chinese School", "/"),
        ("Learn Chinese Characters", "/characters.html"),
        ("All 300 characters", "/learn/characters/"),
        (f"{ch} ({py})", path),
    ])

    explorer_q = f"../../characters.html?ch={esc(ch)}#explorer"

    body = f"""{nav_html()}
<main class="wrap">
  <p class="crumbs"><a href="../../index.html">Home</a> › <a href="../../characters.html">Learn Chinese Characters</a> › <a href="index.html">All 300 characters</a> › <span lang="zh-Hans">{esc(ch)}</span></p>

  <h1><span class="zh" lang="zh-Hans">{esc(ch)}</span> <span class="py">{esc(py)}</span> — “{esc(en)}”</h1>
  <p class="sub">How to write and say the Chinese character <span class="zh" lang="zh-Hans">{esc(ch)}</span> ({esc(py)}), which means <strong>{esc(en)}</strong> — with stroke order, audio, its story, and an example sentence. Theme: {esc(d["group"])}.</p>

  <div class="card hero-grid">
    {glyph_svg(d)}
    <div class="facts">
      <div><span class="lbl">Pinyin · 拼音</span> {esc(py)}</div>
      <div><span class="lbl">Meaning · 意思</span> {esc(en)}</div>
      <div><span class="lbl">Strokes · 笔画</span> {n}</div>
      <div><span class="lbl">Radical · 部首</span> <span class="zh-big" lang="zh-Hans">{esc(d["radical"])}</span> ({esc(d["radEn"])})</div>
      <div class="say-row">
        <span class="lbl" style="width:100%">Hear it · 听发音</span>
        <audio controls preload="none" src="../audio/char-{i}.mp3"></audio>
      </div>
      <div><a class="cta" href="{explorer_q}">Watch it drawn stroke by stroke →</a></div>
    </div>
  </div>

  <h2>Stroke order<span class="zh" lang="zh-Hans">笔顺</span></h2>
  <p class="sub">{esc(ch)} is written with {n} {stroke_word}, in this order (the red stroke is the one being added):</p>
  <div class="strip">{stroke_strip(d)}</div>

  <h2>The story behind it<span class="zh" lang="zh-Hans">字源小故事</span></h2>
  <p class="origin">{esc(d["origin"])}</p>

  <h2>A common word<span class="zh" lang="zh-Hans">常用词</span></h2>
  <div class="card">
    <p class="zh-line">{ruby(d["word"]["seg"])}</p>
    <p class="mean">{esc(word_en)}</p>
    <div class="say-row"><audio controls preload="none" src="../audio/word-{i}.mp3"></audio></div>
  </div>

  <h2>Example sentence<span class="zh" lang="zh-Hans">例句</span></h2>
  <div class="card">
    <p class="zh-line">{ruby(d["ex"]["seg"])}</p>
    <p class="mean">{esc(ex_en)}</p>
    <div class="say-row"><audio controls preload="none" src="../audio/sent-{i}.mp3"></audio></div>
  </div>

  <nav class="pn" aria-label="More characters">
    {prev_link}
    <a href="index.html">All 300 characters</a>
    {next_link}
  </nav>

  <p class="sub" style="margin-top:40px">This page is part of the free
  <a href="../../characters.html">Chinese character explorer</a> from
  <a href="../../index.html">Casey Foundation Chinese School</a> — a Saturday
  community Chinese school in Narre Warren, Victoria, serving Berwick,
  Cranbourne, Hallam and families across Melbourne's southeast.
  New students get a <a href="../../index.html#enrolment">free trial lesson</a>.</p>
</main>
{footer_html()}"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(title, desc, path, og_title=f"{ch} ({py}) — “{en}” · Chinese character stroke order & audio")}
{ld_script(ld)}{ld_script(crumbs)}</head>
<body>
{body}
</body>
</html>
"""


def group_anchor(g):
    return re.sub(r"[^a-z0-9]+", "-", g.lower()).strip("-")


def index_page(data, slugs):
    path = "/learn/characters/"
    title = "300 Chinese Characters for Beginners — Stroke Order, Pinyin & Meaning"
    desc = ("Browse all 300 beginner Chinese characters with pinyin, English meaning, "
            "stroke-order diagrams, audio and example sentences — free, grouped by "
            "theme. From Casey Foundation Chinese School's character explorer.")

    groups = []
    for d in data:
        if d["group"] not in groups:
            groups.append(d["group"])

    ld = {
        "@context": "https://schema.org",
        "@type": ["CollectionPage", "LearningResource"],
        "name": "300 Chinese Characters for Beginners",
        "description": desc,
        "url": SITE + path,
        "inLanguage": ["en", "zh-Hans"],
        "isAccessibleForFree": True,
        "learningResourceType": "Reference",
        "educationalLevel": "Beginner",
        "teaches": "Reading and writing the 300 most useful beginner Chinese characters",
        "hasPart": {"@type": "WebApplication",
                    "name": "识字小馆 — Chinese Character Explorer",
                    "url": f"{SITE}/characters.html"},
        "provider": {"@type": "EducationalOrganization", "@id": f"{SITE}/#school",
                     "name": "Casey Foundation Chinese School", "url": SITE},
    }
    crumbs = breadcrumb_ld([
        ("Casey Foundation Chinese School", "/"),
        ("Learn Chinese Characters", "/characters.html"),
        ("All 300 characters", path),
    ])

    toc = "".join(
        f'<a href="#{group_anchor(g)}">{esc(g)} <span lang="zh-Hans">{esc(GROUP_ZH.get(g, ""))}</span></a>'
        for g in groups
    )

    sections = []
    for g in groups:
        items = "".join(
            f'<li><a href="{slugs[i]}.html">'
            f'<span class="zh" lang="zh-Hans">{esc(d["ch"])}</span>'
            f'<span class="py">{esc(d["py"])}</span>'
            f'<span class="en">{esc(d["en"])}</span></a></li>'
            for i, d in enumerate(data) if d["group"] == g
        )
        zh = GROUP_ZH.get(g, "")
        sections.append(
            f'<h2 id="{group_anchor(g)}">{esc(g)}<span class="zh" lang="zh-Hans">{esc(zh)}</span></h2>'
            f'<ul class="char-list">{items}</ul>'
        )

    body = f"""{nav_html()}
<main class="wrap">
  <p class="crumbs"><a href="../../index.html">Home</a> › <a href="../../characters.html">Learn Chinese Characters</a> › All 300 characters</p>
  <h1>300 Chinese characters, <span class="zh" lang="zh-Hans">一字一页</span></h1>
  <p class="sub">Every character in our free <a href="../../characters.html">interactive
  character explorer</a> has its own reference page: animated-grid glyph, stroke order,
  pinyin, meaning, the story behind the character, a common word and an example
  sentence — all with Mandarin audio. Pick a theme below, or
  <a href="../../characters.html">practise them interactively</a>.</p>
  <div class="toc">{toc}</div>
  {"".join(sections)}
  <p class="sub" style="margin-top:40px">Made by <a href="../../index.html">Casey Foundation
  Chinese School</a>, a Saturday community Chinese school in Narre Warren, Victoria.
  Come and learn with us — the first lesson is <a href="../../index.html#enrolment">a free trial</a>.</p>
</main>
{footer_html()}"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(title, desc, path, og_title="All 300 beginner Chinese characters — free stroke order & audio reference")}
{ld_script(ld)}{ld_script(crumbs)}</head>
<body>
{body}
</body>
</html>
"""


def sitemap(slugs):
    def url(loc, freq, pri):
        return (f"  <url>\n    <loc>{SITE}{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
                f"    <changefreq>{freq}</changefreq>\n    <priority>{pri}</priority>\n  </url>\n")

    out = ['<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n']
    out.append(url("/", "monthly", "1.0"))
    out.append(url("/characters.html", "weekly", "0.8"))
    out.append(url("/learn/characters/", "weekly", "0.7"))
    for slug in slugs:
        out.append(url(f"/learn/characters/{slug}.html", "monthly", "0.5"))
    out.append("</urlset>\n")
    return "".join(out)


def main():
    data = load_data()
    os.makedirs(OUT_DIR, exist_ok=True)

    # stable slugs
    used, slugs = set(), []
    for d in data:
        slugs.append(slugify(d, used))

    # audio must exist for every index we reference
    missing = [f"learn/audio/{k}-{i}.mp3"
               for i in range(len(data)) for k in ("char", "word", "sent")
               if not os.path.exists(f"learn/audio/{k}-{i}.mp3")]
    if missing:
        sys.exit("missing audio files (run scripts/gen-audio.py first):\n  "
                 + "\n  ".join(missing[:10]))

    # remove stale generated pages
    for f in os.listdir(OUT_DIR):
        if f.endswith(".html"):
            os.remove(os.path.join(OUT_DIR, f))

    for i, d in enumerate(data):
        prev_i = (i - 1) % len(data)
        next_i = (i + 1) % len(data)
        prev_link = (f'<a href="{slugs[prev_i]}.html" rel="prev">← <span class="zh" '
                     f'lang="zh-Hans">{esc(data[prev_i]["ch"])}</span> {esc(data[prev_i]["py"])}</a>')
        next_link = (f'<a href="{slugs[next_i]}.html" rel="next"><span class="zh" '
                     f'lang="zh-Hans">{esc(data[next_i]["ch"])}</span> {esc(data[next_i]["py"])} →</a>')
        page = char_page(d, i, slugs[i], prev_link, next_link)
        with open(os.path.join(OUT_DIR, slugs[i] + ".html"), "w", encoding="utf-8") as f:
            f.write(page)

    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page(data, slugs))

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap(slugs))

    print(f"wrote {len(data)} character pages + index to {OUT_DIR}/, regenerated sitemap.xml")


if __name__ == "__main__":
    main()
