#!/usr/bin/env python3
"""Wiki Search & Telegram Card Formatter for Baza (LLM Wiki).
Supports:
  - list_recent(limit=10): overview of sections and recently updated notes
  - search(query, limit=5): full-text and tag/title search with snippets and related links
  - get_page(slug): detailed card of a specific note with metadata, excerpt, and related pages
"""

import os
import re
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

VAULT_DIR = Path(os.environ.get("WIKI_PATH", "/home/ubuntu/baza")).resolve()
BASE_URL = os.environ.get("BAZA_BASE_URL", "https://baza.stepan8nsky.casacam.net")

EXCLUDE_DIRS = {".git", ".obsidian", "_site", "_archive", "scripts", "__pycache__"}
SERVED_DIRS = ["entities", "concepts", "comparisons", "queries", "raw/transcripts", "raw/articles"]

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")

def parse_frontmatter_and_body(text: str):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except Exception:
                fm = {}
            body = parts[2].strip()
            return fm, body
    return {}, text.strip()

def get_all_notes():
    notes = []
    for root, dirs, files in os.walk(VAULT_DIR):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDE_DIRS]
        for f in files:
            if f.endswith(".md") and not f.startswith(".") and f not in {"SCHEMA.md", "log.md", "index.md", "dashboard.md"}:
                fp = Path(root) / f
                rel_path = str(fp.relative_to(VAULT_DIR)).replace("\\", "/")
                slug = fp.stem
                try:
                    text = fp.read_text(encoding="utf-8", errors="replace")
                    fm, body = parse_frontmatter_and_body(text)
                    mtime = datetime.fromtimestamp(fp.stat().st_mtime).strftime("%Y-%m-%d")
                    title = fm.get("title") or re.sub(r"^#\s+", "", body.splitlines()[0]) if body.splitlines() else slug
                    title = re.sub(r"[#*`]", "", str(title)).strip()
                    tags = fm.get("tags") or []
                    if isinstance(tags, str):
                        tags = [t.strip() for t in tags.strip("[]").split(",")]
                    category = rel_path.split("/")[0]
                    if rel_path.startswith("raw/"):
                        category = "raw/" + rel_path.split("/")[1]

                    # extract wikilinks from body and related
                    links = []
                    for match in WIKILINK_RE.finditer(body):
                        target = match.group(1).strip()
                        label = match.group(2) or target.split("/")[-1]
                        links.append((target, label.strip()))

                    notes.append({
                        "file_path": str(fp),
                        "rel_path": rel_path,
                        "slug": slug,
                        "title": title,
                        "category": category,
                        "tags": tags,
                        "updated": fm.get("updated") or mtime,
                        "created": fm.get("created") or mtime,
                        "body": body,
                        "links": links
                    })
                except Exception:
                    continue
    return notes

def clean_snippet(text: str, max_chars: int = 450):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("---") or line.startswith("```"):
            continue
        # replace wikilinks with simple text
        line = WIKILINK_RE.sub(r"\2" if r"\2" else r"\1", line)
        line = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", line)
        line = re.sub(r"\[\[([^\]]+)\]\]", r"\1", line)
        lines.append(line)
        if sum(len(l) for l in lines) >= max_chars:
            break
    snippet = " ".join(lines)
    if len(snippet) > max_chars:
        snippet = snippet[:max_chars].rstrip() + "..."
    return snippet

def format_card(note: dict) -> str:
    slug = note["slug"]
    title = note["title"]
    cat = note["category"]
    updated = note["updated"]
    url = f"{BASE_URL}/{slug}"
    
    snippet = clean_snippet(note["body"])
    
    # build related links
    related_items = []
    seen = set()
    for target, label in note["links"][:5]:
        target_slug = target.split("/")[-1]
        if target_slug not in seen and target_slug != slug:
            seen.add(target_slug)
            related_items.append(f"[{label}]({BASE_URL}/{target_slug})")
    
    related_str = ", ".join(related_items) if related_items else "—"
    
    card = (
        f"**{title}**\n"
        f"📂 *Раздел:* `{cat}` | 🗓 *Обновлено:* `{updated}`\n\n"
        f"{snippet}\n\n"
        f"🔗 [Читать полностью на веб-витрине]({url})\n"
        f"📎 *Связанные страницы:* {related_str}"
    )
    return card

def list_overview():
    notes = get_all_notes()
    # sort by updated desc
    notes.sort(key=lambda x: str(x["updated"]), reverse=True)
    
    total = len(notes)
    categories = {}
    for n in notes:
        cat = n["category"]
        categories[cat] = categories.get(cat, 0) + 1
        
    cats_str = "\n".join([f"• `{cat}`: **{count}** страниц" for cat, count in categories.items()])
    
    recent_list = []
    for n in notes[:8]:
        url = f"{BASE_URL}/{n['slug']}"
        recent_list.append(f"• [{n['title']}]({url}) (`{n['category']}`, {n['updated']})")
    
    recent_str = "\n".join(recent_list)
    
    res = (
        f"🧠 **Оглавление Baza Wiki** (всего: **{total}** страниц)\n\n"
        f"📁 **Разделы базы знаний:**\n{cats_str}\n\n"
        f"🕒 **Недавно обновленные заметки:**\n{recent_str}\n\n"
        f"💡 *Используй `/wiki <запрос>` для поиска или `/wiki <slug>` для открытия.*"
    )
    return res

def search_notes(query: str, limit: int = 5):
    notes = get_all_notes()
    query_lower = query.lower().strip()
    words = query_lower.split()
    
    scored = []
    for n in notes:
        score = 0
        title_lower = n["title"].lower()
        slug_lower = n["slug"].lower()
        body_lower = n["body"].lower()
        tags_lower = [str(t).lower() for t in n["tags"]]
        
        # exact match in slug or title
        if query_lower == slug_lower or query_lower == title_lower:
            score += 100
        elif query_lower in title_lower:
            score += 50
        elif any(query_lower in t for t in tags_lower):
            score += 30
            
        for w in words:
            if w in title_lower:
                score += 20
            if any(w in t for t in tags_lower):
                score += 15
            if w in slug_lower:
                score += 10
            if w in body_lower:
                score += body_lower.count(w)
                
        if score > 0:
            scored.append((score, n))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [item[1] for item in scored[:limit]]
    
    if not results:
        return f"🔍 По запросу *«{query}»* в базе знаний ничего не найдено.\nПопробуй изменить ключевые слова или введи `/wiki` для оглавления."
    
    cards = []
    for i, n in enumerate(results, 1):
        url = f"{BASE_URL}/{n['slug']}"
        snippet = clean_snippet(n["body"], max_chars=200)
        cards.append(f"**{i}. [{n['title']}]({url})** (`{n['category']}`, {n['updated']})\n{snippet}")
        
    res = (
        f"🔍 **Результаты поиска по запросу:** *«{query}»* ({len(scored)} найдено, показаны топ-{len(results)}):\n\n"
        + "\n\n".join(cards) +
        f"\n\n💡 *Чтобы открыть страницу подробно: `/wiki <slug>`*"
    )
    return res

def get_single_page(slug: str):
    slug_clean = slug.strip().lower().replace(".md", "")
    notes = get_all_notes()
    for n in notes:
        if n["slug"].lower() == slug_clean or n["rel_path"].lower() == slug_clean or n["rel_path"].lower() == f"{slug_clean}.md":
            return format_card(n)
        
    # fallback search
    for n in notes:
        if slug_clean in n["slug"].lower() or slug_clean in n["title"].lower():
            return format_card(n)
            
    return f"❌ Страница `{slug}` не найдена в базе знаний.\nВведи `/wiki` для оглавления или `/wiki {slug}` для поиска похожих."

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] in {"--overview", "/wiki", "overview"}:
        print(list_overview())
    elif sys.argv[1] in {"--slug", "page"} and len(sys.argv) > 2:
        print(get_single_page(sys.argv[2]))
    else:
        query = " ".join(sys.argv[1:])
        if query.startswith("/wiki"):
            query = query[5:].strip()
        if not query:
            print(list_overview())
        elif len(query.split()) == 1 and ("-" in query or "_" in query) and not any(ch in query for ch in " +="):
            # check if exact slug
            res = get_single_page(query)
            if not res.startswith("❌"):
                print(res)
            else:
                print(search_notes(query))
        else:
            print(search_notes(query))
