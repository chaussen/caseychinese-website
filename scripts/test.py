#!/usr/bin/env python3
"""
Regression test suite for caseychinese.org (static site, no build step).

Run from the repo root:  python3 scripts/test.py
Exits 0 on pass, 1 on any failure.
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

failures = []
passes = []

def fail(msg):
    failures.append(msg)

def ok(msg):
    passes.append(msg)


# ---------------------------------------------------------------------------
# 1. Local href/src references resolve
# ---------------------------------------------------------------------------
def check_local_refs():
    bad = []
    for f in sorted(glob.glob("*.html")):
        html = open(f, encoding="utf-8").read()
        for ref in re.findall(r'(?:src|href)="([^"#]+)"', html):
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
                continue
            path = ref.split("?")[0].lstrip("/")
            if path and not os.path.exists(path):
                bad.append(f"  {f}: missing {ref}")
    if bad:
        fail("Broken local references:\n" + "\n".join(bad))
    else:
        ok("All local href/src references resolve")

check_local_refs()


# ---------------------------------------------------------------------------
# 2. No HTML tags embedded inside .js files
#    (the bug that caused </script> to appear inside js/index.js)
# ---------------------------------------------------------------------------
def check_js_no_html_tags():
    bad = []
    for f in sorted(glob.glob("js/*.js")):
        src = open(f, encoding="utf-8").read()
        for i, line in enumerate(src.splitlines(), 1):
            if re.search(r'</?script', line, re.IGNORECASE):
                bad.append(f"  {f}:{i}: {line.strip()}")
    if bad:
        fail("HTML <script> tags found inside JS files:\n" + "\n".join(bad))
    else:
        ok("No HTML tags embedded in JS files")

check_js_no_html_tags()


# ---------------------------------------------------------------------------
# 3. JS files pass Node.js syntax check
# ---------------------------------------------------------------------------
def check_js_syntax():
    bad = []
    for f in sorted(glob.glob("js/*.js")):
        result = subprocess.run(
            ["node", "--check", f],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            msg = (result.stderr or result.stdout).strip().splitlines()[0]
            bad.append(f"  {f}: {msg}")
    if bad:
        fail("JS syntax errors:\n" + "\n".join(bad))
    else:
        ok("All JS files pass syntax check")

check_js_syntax()


# ---------------------------------------------------------------------------
# 4. No unsafe inline scripts in HTML
#    Inline <script> blocks (without src= or type=application/ld+json) must
#    not exist in pages that have a strict CSP (script-src without unsafe-inline).
# ---------------------------------------------------------------------------
def check_no_inline_scripts():
    bad = []
    for f in sorted(glob.glob("*.html")):
        html = open(f, encoding="utf-8").read()

        # Does this page have a CSP that excludes unsafe-inline?
        csp_match = re.search(r'Content-Security-Policy[^>]*content="([^"]+)"', html)
        if not csp_match:
            continue
        csp = csp_match.group(1)
        script_src = re.search(r'script-src\s+([^;]+)', csp)
        if not script_src or "'unsafe-inline'" in script_src.group(1):
            continue  # no strict script-src, skip

        # Find inline <script> blocks (no src=, not ld+json)
        for m in re.finditer(r'<script([^>]*)>([\s\S]*?)</script>', html):
            attrs = m.group(1)
            if 'src=' in attrs:
                continue
            if 'application/ld+json' in attrs:
                continue
            snippet = m.group(2).strip()[:60].replace('\n', ' ')
            bad.append(f"  {f}: inline script — {snippet!r}")

    if bad:
        fail("Inline scripts present in pages with strict CSP (would be blocked):\n" + "\n".join(bad))
    else:
        ok("No unsafe inline scripts in strict-CSP pages")

check_no_inline_scripts()


# ---------------------------------------------------------------------------
# 5. getElementById / querySelector ID contract
#    Every getElementById('X') in a JS file must have a matching id="X" in
#    the HTML file(s) that load it.
# ---------------------------------------------------------------------------
JS_TO_HTML = {
    "js/index.js":      ["index.html"],
    "js/characters.js": ["characters.html"],
    "js/gtag-init.js":  [],   # no DOM access
}

def collect_html_ids(html_files):
    ids = set()
    for f in html_files:
        if not os.path.exists(f):
            continue
        html = open(f, encoding="utf-8").read()
        ids.update(re.findall(r'\bid="([^"]+)"', html))
    return ids

def check_id_contract():
    bad = []
    for js_file, html_files in JS_TO_HTML.items():
        if not os.path.exists(js_file) or not html_files:
            continue
        js_src = open(js_file, encoding="utf-8").read()
        html_ids = collect_html_ids(html_files)
        for m in re.finditer(r"getElementById\(['\"]([^'\"]+)['\"]\)", js_src):
            el_id = m.group(1)
            if el_id not in html_ids:
                bad.append(f"  {js_file}: getElementById('{el_id}') — id not found in {html_files}")
    if bad:
        fail("getElementById calls reference missing HTML ids:\n" + "\n".join(bad))
    else:
        ok("All getElementById calls match HTML ids")

check_id_contract()


# ---------------------------------------------------------------------------
# 6. Script src= files actually exist (belt-and-suspenders over check 1)
# ---------------------------------------------------------------------------
def check_script_src_files():
    bad = []
    for f in sorted(glob.glob("*.html")):
        html = open(f, encoding="utf-8").read()
        for src in re.findall(r'<script[^>]+src="([^"]+)"', html):
            if src.startswith(("http://", "https://", "//")):
                continue
            path = src.lstrip("/")
            if not os.path.exists(path):
                bad.append(f"  {f}: <script src=\"{src}\"> file missing")
    if bad:
        fail("Missing script src files:\n" + "\n".join(bad))
    else:
        ok("All <script src=> files exist")

check_script_src_files()


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
print()
for p in passes:
    print(f"  \033[32m✓\033[0m  {p}")
if failures:
    print()
    for f in failures:
        first, *rest = f.splitlines()
        print(f"  \033[31m✗\033[0m  {first}")
        for r in rest:
            print(f"       {r}")
    print(f"\n{len(failures)} check(s) failed, {len(passes)} passed.\n")
    sys.exit(1)
else:
    print(f"\n  All {len(passes)} checks passed.\n")
