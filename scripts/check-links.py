#!/usr/bin/env python3
"""Fail if any local src/href in the HTML files points at a missing file.

Covers the hand-written pages at the repo root and the generated character
pages under learn/characters/. Relative references are resolved against the
directory of the file that contains them.
"""
import glob
import os
import re
import sys

bad = []
for f in sorted(glob.glob("*.html") + glob.glob("learn/characters/*.html")):
    html = open(f, encoding="utf-8").read()
    base = os.path.dirname(f)
    for ref in re.findall(r'(?:src|href)="([^"#]+)"', html):
        if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
            continue
        path = ref.split("?")[0]
        if path.startswith("/"):
            path = path.lstrip("/")
        else:
            path = os.path.normpath(os.path.join(base, path))
        if path and not os.path.exists(path):
            bad.append(f"{f}: {ref}")

if bad:
    print("Broken local references:")
    print("\n".join("  " + b for b in bad))
    sys.exit(1)
print("All local references resolve.")
