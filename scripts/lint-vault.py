#!/usr/bin/env python3
"""Lint Baza vault using the llm-wiki/Obsidian conventions.

Checks are intentionally scoped to the editable wiki layer. raw/ and _archive/
are kept for provenance and history, so old links there do not fail the public
site build. Code spans/blocks are ignored before parsing wikilinks.
"""
import os
import re
import sys
from pathlib import Path

vault = Path(__file__).resolve().parents[1]
errors = []
warnings = []

WIKI_DIRS = {"entities", "concepts", "comparisons", "queries"}
SERVICE_FILES = {"index.md", "SCHEMA.md", "log.md", "dashboard.md"}
ORPHAN_EXEMPT = {"index.md", "SCHEMA.md", "log.md"}
LOW_OUTBOUND_EXEMPT = {"index.md", "SCHEMA.md", "log.md"}


def is_excluded(path: Path) -> bool:
    parts = set(path.relative_to(vault).parts)
    return bool(parts & {".git", ".obsidian", "_site", "_archive", ".hermes"})


def all_md_files():
    for fp in vault.rglob("*.md"):
        if not is_excluded(fp):
            yield fp


def wiki_files():
    for fp in all_md_files():
        rel = fp.relative_to(vault)
        if rel.parts[0] in WIKI_DIRS or fp.name in SERVICE_FILES:
            yield fp


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    return text


def wiki_links(text: str):
    text = strip_code(text)
    pattern = r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]"
    for match in re.finditer(pattern, text):
        yield match.group(1).strip().removesuffix(".md")


all_files = list(all_md_files())
editable_files = list(wiki_files())

# --- 1. Encoding ---
for fp in all_files:
    try:
        fp.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        errors.append(f"ENCODING: {fp.relative_to(vault)} — not UTF-8")

# --- 2. Empty notes ---
for fp in all_files:
    text = fp.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) < 10:
        warnings.append(f"EMPTY: {fp.relative_to(vault)} — {len(text)} chars")

# --- 3. Frontmatter for editable wiki layer ---
for fp in editable_files:
    rel = str(fp.relative_to(vault))
    if fp.name in {"SCHEMA.md", "log.md"} or fp.name == "README.md":
        continue
    content = fp.read_text(encoding="utf-8", errors="replace")
    if not content.startswith("---"):
        errors.append(f"FRONTMATTER: {rel} — missing YAML frontmatter")
        continue
    fm = content.split("---", 2)[1] if content.count("---") >= 2 else ""
    for field in ("title:", "type:", "tags:"):
        if field not in fm:
            errors.append(f"FRONTMATTER: {rel} — missing {field}")

# --- 4. Known wikilink targets ---
known_path = {}
known_base = {}
for fp in all_files:
    rel = str(fp.relative_to(vault))
    no_ext = rel[:-3]
    known_path[no_ext] = rel
    known_base[Path(no_ext).name.lower()] = rel
    if Path(no_ext).name == "index":
        parent = str(Path(no_ext).parent)
        if parent and parent != ".":
            known_path[parent] = rel
        else:
            known_path["Home"] = rel

# Allow asset links without extension in raw references.
for asset in vault.glob("raw/assets/**/*"):
    if asset.is_file():
        rel = str(asset.relative_to(vault))
        known_path[str(Path(rel).with_suffix(""))] = rel
        known_base[Path(rel).stem.lower()] = rel

# --- 5. Broken wikilinks in editable wiki layer only ---
for fp in editable_files:
    rel = str(fp.relative_to(vault))
    content = fp.read_text(encoding="utf-8", errors="replace")
    for link in wiki_links(content):
        resolved = known_path.get(link) or known_base.get(Path(link).name.lower())
        if not resolved:
            errors.append(f"BROKEN LINK: {rel} → [[{link}]]")

# --- 6. Orphans and outbound links in editable wiki layer ---
incoming = {str(fp.relative_to(vault)): 0 for fp in editable_files if fp.name != "README.md"}
outbound = {}
for fp in editable_files:
    rel = str(fp.relative_to(vault))
    content = fp.read_text(encoding="utf-8", errors="replace")
    resolved_links = set()
    for link in wiki_links(content):
        resolved = known_path.get(link) or known_base.get(Path(link).name.lower())
        if resolved:
            resolved_links.add(resolved)
            if resolved in incoming and resolved != rel:
                incoming[resolved] += 1
    outbound[rel] = len(resolved_links)

for rel, count in incoming.items():
    if rel not in ORPHAN_EXEMPT and count == 0:
        errors.append(f"ORPHAN: {rel} — 0 incoming links")

for rel, count in outbound.items():
    if rel not in LOW_OUTBOUND_EXEMPT and count < 2:
        errors.append(f"LOW OUTBOUND: {rel} — {count} links (<2)")

# --- Summary ---
print(f"📋 Baza lint — editable wiki: {len(editable_files)} pages; all md: {len(all_files)}")
if errors:
    print(f"❌ {len(errors)} error(s)")
    for e in errors:
        print("- " + e)
if warnings:
    print(f"⚠️ {len(warnings)} warning(s)")
    for w in warnings:
        print("- " + w)
if not errors and not warnings:
    print("✅ Lint passed — 0 issues")
elif not errors:
    print("✅ Lint passed with warnings only")
sys.exit(1 if errors else 0)
