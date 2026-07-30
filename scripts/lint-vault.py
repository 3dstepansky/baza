#!/usr/bin/env python3
"""Lint vault: check wiki-links, encoding, frontmatter, orphans."""
import os, re, sys

vault = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []

def md_files():
    for root, dirs, fnames in os.walk(vault):
        if '.git' in root or '.obsidian' in root or '_site' in root:
            continue
        for f in fnames:
            if f.endswith('.md'):
                yield os.path.join(root, f)

# --- 1. Encoding ---
for fp in md_files():
    with open(fp, 'rb') as fh:
        raw = fh.read()
    try:
        raw.decode('utf-8')
    except UnicodeDecodeError:
        errors.append(f"🔴 ENCODING: {os.path.relpath(fp, vault)} — not UTF-8")

# --- 2. Empty notes ---
for fp in md_files():
    with open(fp, encoding='utf-8') as fh:
        text = fh.read().strip()
    if len(text) < 10:
        errors.append(f"🟡 EMPTY: {os.path.relpath(fp, vault)} — {len(text)} chars")

# --- 3. Frontmatter on index files ---
for fp in md_files():
    rel = os.path.relpath(fp, vault)
    if os.path.basename(fp) == 'index.md':
        with open(fp, encoding='utf-8') as fh:
            content = fh.read()
        if not content.startswith('---'):
            errors.append(f"🔴 FRONTMATTER: {rel} — no frontmatter on index")
        elif 'tags:' not in content.split('---')[1]:
            errors.append(f"🟡 FRONTMATTER: {rel} — no 'tags:' in frontmatter")

# --- 4. Broken wiki-links ---
known_path = {}
known_base = {}
for fp in md_files():
    rel = os.path.relpath(fp, vault)
    no_ext = os.path.splitext(rel)[0]  # "Dev/Python"
    known_path[no_ext] = rel
    simple = os.path.basename(no_ext)  # "Python"
    known_base[simple] = rel
    # Alias: Dev/index.md -> known_path["Dev"]
    if simple == 'index':
        parent = os.path.dirname(no_ext)  # "Dev" or ""
        if parent:
            known_path[parent] = rel
        else:
            known_path['Home'] = rel

for fp in md_files():
    rel = os.path.relpath(fp, vault)
    with open(fp, encoding='utf-8') as fh:
        content = fh.read()
    for m in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content):
        link = m.group(1).strip()
        resolved = known_path.get(link) or known_base.get(link)
        if not resolved:
            errors.append(f"🟡 BROKEN LINK: {rel} → [[{link}]]")

# --- 5. Orphans (no incoming links) ---
incoming = {fp: 0 for fp in md_files()}
for fp in md_files():
    with open(fp, encoding='utf-8') as fh:
        content = fh.read()
    for m in re.finditer(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content):
        link = m.group(1).strip()
        resolved = known_path.get(link) or known_base.get(link)
        if resolved:
            target_fp = os.path.join(vault, resolved)
            incoming[target_fp] = incoming.get(target_fp, 0) + 1

orphan_count = 0
for fp, cnt in incoming.items():
    if cnt == 0:
        rel = os.path.relpath(fp, vault)
        errors.append(f"🟢 ORPHAN: {rel} — 0 incoming links")
        orphan_count += 1

# --- Summary ---
if not errors:
    total = len(list(md_files()))
    print(f"✅ Lint passed — {total} notes, 0 issues")
    sys.exit(0)

print(f"📋 Lint: {len(errors)} issue(s)")
for e in errors:
    print(e)
sys.exit(1 if any(e.startswith('🔴') for e in errors) else 0)
