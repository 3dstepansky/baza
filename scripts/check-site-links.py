#!/usr/bin/env python3
"""Проверка битых ссылок собранного сайта vault (_site/)."""
import re
import sys
from pathlib import Path

VAULT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "baza"
SITE = VAULT / "_site"

if not SITE.exists():
    print(f"Нет _site в {VAULT} — сначала build-site.py")
    sys.exit(2)

broken, total = [], 0
for html in sorted(SITE.rglob("*.html")):
    if "_archive" in html.parts:
        continue
    text = html.read_text(encoding="utf-8")
    for m in re.finditer(r'href="([^"]+)"', text):
        href = m.group(1)
        if href.startswith("http") or href == "/" or href.startswith("#"):
            continue
        total += 1
        target = (html.parent / href).resolve()
        if not target.exists() and not (html.parent / (href + ".html")).exists():
            broken.append(f"{html.relative_to(SITE)} -> {href}")

print(f"Проверено ссылок: {total}")
if broken:
    print(f"Битых: {len(broken)}")
    for b in broken[:50]:
        print("  ✗", b)
    sys.exit(1)
else:
    print("Битых: 0 ✅")
    sys.exit(0)
