#!/usr/bin/env python3
"""Convert vault .md files to a readable static HTML site.
- index.md -> index.html (каталог wiki, НЕ перезаписывается деревом)
- относительные ссылки с учётом глубины (entities/x -> ../concepts/y)
- code-блоки не конвертируются как wikilinks
- raw/ показывается как текст (источники), _archive/ исключён
"""
import os, re, shutil, markdown
from datetime import datetime

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(VAULT, "_site")

CSS = """* { margin:0; padding:0; box-sizing:border-box; }
body { background:#0d1117; color:#c9d1d9; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; line-height:1.7; font-size:16px; }
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
.nav { background:#161b22; border-bottom:1px solid #30363d; padding:8px 16px; font-size:14px; position:sticky; top:0; z-index:10; }
.nav a { color:#58a6ff; }
.meta { font-size:0.85em; color:#8b949e; margin:0.5em 0 1em; }
.tag { display:inline-block; background:#1f6feb33; color:#58a6ff; padding:2px 8px; border-radius:10px; font-size:0.8em; margin:0 3px 3px 0; }
.backlinks { margin-top:2em; padding-top:1em; border-top:1px solid #30363d; }
.backlinks h3 { font-size:1em; color:#8b949e; }
.button-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:10px; margin:1em 0; }
.button { display:block; background:#238636; color:#fff !important; padding:12px 14px; border-radius:8px; text-align:center; font-weight:600; border:1px solid #2ea043; }
.button:hover { background:#2ea043; text-decoration:none; }"""

def wikilink_to_html(match, prefix):
    text = match.group(1)
    parts = text.split('|')
    target = parts[0].strip()
    label = parts[1].strip() if len(parts) > 1 else target.split('/')[-1] or target
    target_html = target
    if not target_html.endswith('.md') and not target_html.endswith('.html'):
        target_html += '.html'
    else:
        target_html = re.sub(r'\.md$', '.html', target_html)
    return f'<a href="{prefix}{target_html}">{label}</a>'

def convert_file(rel_path):
    src = os.path.join(VAULT, rel_path)
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = rel_path.split('/')
    depth = len(parts) - 1
    prefix = '../' * depth

    frontmatter = {}
    body = content
    if content.startswith('---'):
        fm_parts = content.split('---', 2)
        if len(fm_parts) >= 3:
            fm_text = fm_parts[1].strip()
            for line in fm_text.split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    frontmatter[k.strip()] = v.strip().strip(chr(34)).strip(chr(39))
            body = fm_parts[2].strip()

    is_raw = '/raw/' in '/' + rel_path

    # stash code blocks before wikilink conversion
    stash = []
    def stasher(m):
        stash.append(m.group(0))
        return f'@@CODE{len(stash)-1}@@'
    body = re.sub(r'```.*?```', stasher, body, flags=re.S)
    body = re.sub(r'`[^`]*`', stasher, body)

    if not is_raw:
        body = re.sub(r'\[\[([^\]]+)\]\]', lambda m: wikilink_to_html(m, prefix), body)
    else:
        # raw: показать [[...]] как текст
        body = re.sub(r'\[\[([^\]]+)\]\]', r'\1', body)

    for i, cb in enumerate(stash):
        body = body.replace(f'@@CODE{i}@@', cb)

    body = re.sub(r'```dataview\n(.*?)```', r'<div class="dataview">\1</div>', body, flags=re.DOTALL)
    html_body = markdown.markdown(body, extensions=['fenced_code', 'tables', 'codehilite'])

    # breadcrumbs: папки — не ссылки (нет индексных страниц), только 🏠
    crumbs = '<a href="/">🏠</a>'
    if len(parts) > 1:
        path_so_far = []
        for p in parts[:-1]:
            path_so_far.append(p)
            crumbs += f' / <span>{p}</span>'
    breadcrumbs = f'<span class="crumbs">{crumbs}</span>'

    tags_html = ''
    if 'tags' in frontmatter:
        tags = frontmatter['tags'].strip('[]').split(',')
        tags_html = ' '.join(f'<span class="tag">{t.strip()}</span>' for t in tags)

    mtime = os.path.getmtime(src)
    date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')

    title = frontmatter.get('title', os.path.splitext(parts[-1])[0])
    if title == 'index':
        title = 'Home' if len(parts) == 1 else parts[-2]

    # backlinks
    filename = os.path.splitext(os.path.basename(rel_path))[0]
    backlinks_html = ''
    backlinks = []
    for f in all_files:
        if f == rel_path:
            continue
        t = open(os.path.join(VAULT, f), encoding='utf-8').read()
        for m in re.finditer(r'\[\[([^\]|#]+)', t):
            if os.path.splitext(os.path.basename(m.group(1)))[0].lower() == filename.lower():
                backlinks.append(f)
                break
    if backlinks:
        bl = ''.join(f'<li><a href="{prefix}{b.replace(".md", ".html")}">{b}</a></li>' for b in sorted(backlinks)[:10])
        backlinks_html = f'<div class="backlinks"><h3>↩ Обратные ссылки</h3><ul>{bl}</ul></div>'

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Vault</title>
<style>{CSS}</style>
</head>
<body>
<nav class="nav">{breadcrumbs}</nav>
<div class="container">
<h1>{title}</h1>
<div class="meta">{tags_html} last modified: {date_str}</div>
{html_body}
{backlinks_html}
</div>
</body>
</html>"""
    out_path = os.path.join(OUTPUT, re.sub(r'\.md$', '.html', rel_path))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return rel_path

all_files = []

def build_site():
    global all_files
    if os.path.exists(OUTPUT):
        shutil.rmtree(OUTPUT)
    os.makedirs(OUTPUT)
    for root, dirs, fnames in os.walk(VAULT):
        if any(x in root for x in ['.git', '_site', 'scripts', '.hermes', '_archive']):
            continue
        for f in fnames:
            if f.endswith('.md'):
                all_files.append(os.path.relpath(os.path.join(root, f), VAULT))
    all_files.sort()
    converted = []
    for f in all_files:
        try:
            convert_file(f)
            converted.append(f)
        except Exception as e:
            print(f"  ERROR {f}: {e}")
    print(f"Done: {len(converted)} files converted → {OUTPUT}")

if __name__ == '__main__':
    build_site()
