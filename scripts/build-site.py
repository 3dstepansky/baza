#!/usr/bin/env python3
"""Convert vault .md files to a readable static HTML site."""
import os, re, markdown
from datetime import datetime

VAULT = "/home/ubuntu/baza"
OUTPUT = os.path.join(VAULT, "_site")

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body {
  background:#0d1117; color:#c9d1d9; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  line-height:1.7; font-size:16px; padding:0;
}
.container { max-width:820px; margin:0 auto; padding:16px; }
h1 { font-size:1.6em; color:#f0f6fc; margin:0.6em 0 0.4em; border-bottom:1px solid #30363d; padding-bottom:0.3em; }
h2 { font-size:1.25em; color:#f0f6fc; margin:0.8em 0 0.3em; }
h3 { font-size:1.1em; color:#f0f6fc; margin:0.6em 0 0.2em; }
p { margin:0.5em 0; }
a { color:#58a6ff; text-decoration:none; }
a:hover { text-decoration:underline; }
ul, ol { margin:0.5em 0; padding-left:1.5em; }
li { margin:0.3em 0; }
code { background:#161b22; padding:2px 6px; border-radius:3px; font-size:0.9em; color:#f0c674; }
pre { background:#161b22; padding:12px; border-radius:6px; overflow-x:auto; margin:0.8em 0; }
pre code { background:none; padding:0; }
blockquote { border-left:3px solid #30363d; padding-left:1em; margin:0.8em 0; color:#8b949e; }
hr { border:none; border-top:1px solid #30363d; margin:1.2em 0; }
table { width:100%; border-collapse:collapse; margin:0.8em 0; }
th, td { border:1px solid #30363d; padding:8px 12px; text-align:left; }
th { background:#161b22; color:#f0f6fc; }
.dataview { background:#161b22; border:1px solid #30363d; border-radius:6px; padding:12px; margin:0.8em 0; font-family:monospace; font-size:0.85em; color:#8b949e; }
.nav { background:#161b22; border-bottom:1px solid #30363d; padding:8px 16px; display:flex; gap:12px; flex-wrap:wrap; align-items:center; font-size:14px; position:sticky; top:0; z-index:10; }
.nav a { color:#58a6ff; }
.nav .crumbs { color:#8b949e; }
.nav .crumbs a { color:#8b949e; }
.nav .crumbs a:hover { color:#58a6ff; }
.meta { font-size:0.85em; color:#8b949e; margin:0.5em 0 1em; }
.tag { display:inline-block; background:#1f6feb33; color:#58a6ff; padding:2px 8px; border-radius:10px; font-size:0.8em; margin:0 3px 3px 0; }
.backlinks { margin-top:2em; padding-top:1em; border-top:1px solid #30363d; }
.backlinks h3 { font-size:1em; color:#8b949e; }
"""

def wikilink_to_html(match):
    """Convert [[Wiki Link]] to HTML link."""
    text = match.group(1)
    parts = text.split('|')
    target = parts[0].strip()
    label = parts[1].strip() if len(parts) > 1 else target.split('/')[-1] or target
    # Keep .md extension for the file
    target_html = target
    if not target_html.endswith('.md') and not target_html.endswith('.html'):
        target_html += '.html'
    else:
        target_html = re.sub(r'\.md$', '.html', target_html)
    return f'<a href="{target_html}">{label}</a>'

def convert_file(rel_path):
    """Convert a .md file to .html."""
    src = os.path.join(VAULT, rel_path)
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    frontmatter = {}
    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            for line in fm_text.split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    frontmatter[k.strip()] = v.strip().strip('"').strip("'")
            body = parts[2].strip()
    
    # Convert [[wikilinks]]
    body = re.sub(r'\[\[([^\]]+)\]\]', wikilink_to_html, body)
    
    # Remove ```dataview blocks (show as plain)
    body = re.sub(r'```dataview\n(.*?)```', r'<div class="dataview">\1</div>', body, flags=re.DOTALL)
    
    # Convert markdown to HTML
    html_body = markdown.markdown(body, extensions=['fenced_code', 'tables', 'codehilite'])
    
    # Build breadcrumbs
    parts = rel_path.split('/')
    breadcrumbs = '<a href="/">🏠</a>'
    if len(parts) > 1:
        for i, p in enumerate(parts[:-1]):
            up = '/'.join(parts[:i+1])
            breadcrumbs += f' / <a href="/{up}/">{p}</a>'
    
    # Tags from frontmatter
    tags_html = ''
    if 'tags' in frontmatter:
        tags = frontmatter['tags'].strip('[]').split(',')
        tags_html = ' '.join(f'<span class="tag">{t.strip()}</span>' for t in tags)
    
    # Get file mtime
    mtime = os.path.getmtime(src)
    date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
    
    # Find backlinks (files that link to this file)
    filename = os.path.splitext(os.path.basename(rel_path))[0]
    backlinks_html = ''
    
    title = frontmatter.get('title', os.path.splitext(parts[-1])[0])
    # Capitalize title
    if title == 'index':
        # Make title from parent folder name
        if len(parts) > 1:
            title = parts[-2]
        else:
            title = 'Home'
    
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Vault</title>
<style>{CSS}</style>
</head>
<body>
<nav class="nav"><span class="crumbs">{breadcrumbs}</span></nav>
<div class="container">
<h1>{title}</h1>
<div class="meta">{tags_html} last modified: {date_str}</div>
{html_body}
{backlinks_html}
</div>
</body>
</html>"""
    
    # Write output
    out_path = os.path.join(OUTPUT, re.sub(r'\.md$', '.html', rel_path))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return rel_path

def build_site():
    """Build the entire site."""
    import shutil
    if os.path.exists(OUTPUT):
        shutil.rmtree(OUTPUT)
    os.makedirs(OUTPUT)
    
    files = []
    for root, dirs, fnames in os.walk(VAULT):
        if '.git' in root or '_site' in root or 'scripts' in root or '.hermes' in root:
            continue
        for f in fnames:
            if not f.endswith('.md'):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, VAULT)
            files.append(rel)
    
    files.sort()
    converted = []
    for f in files:
        try:
            convert_file(f)
            converted.append(f)
        except Exception as e:
            print(f"  ERROR {f}: {e}")
    
    # Generate index.html at root
    generate_index(files, converted)
    
    print(f"\nDone: {len(converted)} files converted → {OUTPUT}")

def generate_index(all_files, converted):
    """Generate root index.html with file tree."""
    tree_html = '<ul>'
    dirs_seen = set()
    for f in sorted(all_files):
        parts = f.split('/')
        if len(parts) > 1:
            d = parts[0]
            if d not in dirs_seen:
                dirs_seen.add(d)
                tree_html += f'<li>📁 <a href="{d}/">{d}</a></li>'
        else:
            name = os.path.splitext(parts[0])[0]
            tree_html += f'<li>📄 <a href="{f.replace(".md",".html")}">{name}</a></li>'
    tree_html += '</ul>'
    
    # Recent files
    recent = []
    for f in all_files:
        src = os.path.join(VAULT, f)
        mtime = os.path.getmtime(src)
        recent.append((mtime, f))
    recent.sort(reverse=True)
    
    recent_html = '<ol>'
    for mtime, f in recent[:10]:
        d = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        name = os.path.splitext(f.split('/')[-1])[0]
        recent_html += f'<li><a href="{f.replace(".md",".html")}">{f}</a> <small>{d}</small></li>'
    recent_html += '</ol>'
    
    index = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vault — LLM Wiki</title>
<style>{CSS}
.hero {{ text-align:center; padding:2em 0 1em; }}
.hero h1 {{ font-size:2em; border:none; }}
.hero p {{ color:#8b949e; }}
.columns {{ display:flex; flex-wrap:wrap; gap:24px; }}
.column {{ flex:1; min-width:280px; }}
</style>
</head>
<body>
<div class="container">
<div class="hero">
<h1>🗂️ Vault</h1>
<p>LLM Wiki · {len(converted)} notes</p>
</div>
<div class="columns">
<div class="column">
<h2>📂 Структура</h2>
{tree_html}
</div>
<div class="column">
<h2>🕐 Последние</h2>
{recent_html}
</div>
</div>
<p style="margin-top:2em;text-align:center;color:#8b949e;font-size:0.85em">
📊 <a href="/vault-graph.html">Граф связей</a>
</p>
</div>
</body>
</html>"""
    with open(os.path.join(OUTPUT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index)
    print(f"  index.html — {len(converted)} notes")

if __name__ == '__main__':
    build_site()
