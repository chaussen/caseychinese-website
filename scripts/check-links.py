#!/usr/bin/env python3
"""Fail if any local src/href in the HTML files points at a missing file."""
import glob
import os
import re
import sys

bad = []
for f in sorted(glob.glob("*.html")):
    html = open(f, encoding="utf-8").read()
    for ref in re.findall(r'(?:src|href)="([^"#]+)"', html):
        if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
            continue
        path = ref.split("?")[0].lstrip("/")
        if path and not os.path.exists(path):
            bad.append(f"{f}: {ref}")

if bad:
    print("Broken local references:")
    print("\n".join("  " + b for b in bad))
    sys.exit(1)
print("All local references resolve.")
