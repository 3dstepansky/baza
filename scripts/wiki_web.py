#!/usr/bin/env python3
"""Live read-only Baza wiki web server.

No static build: markdown is rendered on each GET. The vault stays the single
source of truth; after a page is changed, the next request sees the new text.

Security model:
- read-only HTTP API: POST/PUT/PATCH/DELETE return 405;
- route validation rejects traversal and non-wiki paths;
- inline rendering escapes all user/vault text before adding renderer-owned tags;
- broken wikilinks are rendered as plain text, not broken <a> tags.

Run:
  python3 scripts/wiki_web.py --bind 0.0.0.0 --port 8383
"""
from __future__ import annotations

import argparse
import html as _h
import os
import re
import sys
import traceback
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable

VAULT = Path(os.environ.get("WIKI_PATH", Path(__file__).resolve().parents[1])).resolve()
SERVED_DIRS = {"entities", "concepts", "comparisons", "queries"}
ROOT_PAGES = {"index.md", "SCHEMA.md", "log.md", "dashboard.md"}
EXCLUDED_PARTS = {".git", ".obsidian", "_site", "_archive", ".hermes", "scripts", "tests", "__pycache__"}

SLUG_OK = re.compile(r"^[\w\-]+$", re.UNICODE)
PATH_OK = re.compile(r"^[\w\-/]+$", re.UNICODE)
FILE_OK = re.compile(r"^[\w\-]+\.md$", re.UNICODE)
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
PROVENANCE = re.compile(r"\^\[([^\]]+)\]")
MD_LINK = re.compile(r"\[([^\]]+)\]\((/[^)]+)\)")

CSS = """
*{box-sizing:border-box} body{margin:0;background:#0d1117;color:#c9d1d9;font:16px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif}
a{color:#58a6ff;text-decoration:none} a:hover{text-decoration:underline}.nav{position:sticky;top:0;background:#161b22;border-bottom:1px solid #30363d;padding:9px 16px;z-index:10}.nav a{margin-right:14px}.container{max-width:920px;margin:0 auto;padding:18px}h1,h2,h3,h4{color:#f0f6fc;line-height:1.25}h1{font-size:1.7em;border-bottom:1px solid #30363d;padding-bottom:.3em}h2{margin-top:1.1em;font-size:1.35em}h3{font-size:1.15em}p{margin:.55em 0}ul{padding-left:1.4em}li{margin:.25em 0}blockquote{border-left:3px solid #30363d;margin:.8em 0;padding:.15em 1em;color:#9ca3af;background:#111827}code{background:#161b22;color:#f0c674;border-radius:4px;padding:2px 5px}pre{background:#161b22;border:1px solid #30363d;border-radius:7px;padding:12px;overflow:auto}pre code{background:transparent;padding:0}table{border-collapse:collapse;width:100%;margin:1em 0;display:block;overflow-x:auto}th,td{border:1px solid #30363d;padding:8px 10px;text-align:left;vertical-align:top}th{background:#161b22;color:#f0f6fc}.meta{color:#8b949e;font-size:.88em;margin:.4em 0 1em}.tag{display:inline-block;background:#1f6feb33;color:#58a6ff;border-radius:999px;padding:2px 8px;margin-right:4px}.missing{color:#f0c674}.src{font-size:.75em}.err{background:#2b1111;border:1px solid #7f1d1d;padding:12px;border-radius:8px}.small{font-size:.9em;color:#8b949e}
"""

@dataclass(frozen=True)
class Page:
    path: Path
    rel: str
    slug: str
    front: dict[str, str]
    body: str


def _now_msk() -> str:
    return datetime.now(timezone(timedelta(hours=3))).strftime("%Y-%m-%d %H:%M:%S MSK")


def _slugify(text: str) -> str:
    text = text.strip().lower().replace("ё", "е")
    text = re.sub(r"[^\w\-]+", "-", text, flags=re.UNICODE)
    return re.sub(r"-+", "-", text).strip("-") or "section"


def _is_excluded(path: Path) -> bool:
    try:
        rel = path.relative_to(VAULT)
    except ValueError:
        return True
    return bool(set(rel.parts) & EXCLUDED_PARTS)


def _iter_md() -> Iterable[Path]:
    for fp in VAULT.rglob("*.md"):
        if _is_excluded(fp):
            continue
        rel = fp.relative_to(VAULT)
        if rel.name in ROOT_PAGES or rel.parts[0] in SERVED_DIRS or rel.parts[0] == "raw":
            yield fp


def _split_front(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    front: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        front[k.strip()] = v.strip().strip('"').strip("'")
    return front, parts[2].lstrip("\n")


def _page_from_path(fp: Path) -> Page:
    text = fp.read_text(encoding="utf-8", errors="replace")
    front, body = _split_front(text)
    rel = str(fp.relative_to(VAULT)).replace(os.sep, "/")
    slug = fp.stem if fp.name != "index.md" else "index"
    return Page(fp, rel, slug, front, body)


def _served_pages(include_raw: bool = False) -> list[Path]:
    pages = []
    for fp in _iter_md():
        rel = fp.relative_to(VAULT)
        if rel.parts[0] == "raw" and not include_raw:
            continue
        front, _ = _split_front(fp.read_text(encoding="utf-8", errors="replace"))
        if front.get("draft", "").lower() == "true" or front.get("status", "").lower() == "draft":
            continue
        pages.append(fp)
    return sorted(pages)


def _find(target: str) -> Page | None:
    target = urllib.parse.unquote(target).strip("/")
    if target in {"", "index", "index.html"}:
        fp = VAULT / "index.md"
        return _page_from_path(fp) if fp.exists() else None
    target = re.sub(r"\.html$", "", target)
    target = re.sub(r"\.md$", "", target)
    if not PATH_OK.fullmatch(target) or ".." in target.split("/"):
        return None

    candidates: list[Path] = []
    # Explicit path: entities/foo or raw/articles/foo
    candidates.append(VAULT / f"{target}.md")
    # Root page by basename: construction-maps-mcp -> entities/construction-maps-mcp.md
    if "/" not in target and SLUG_OK.fullmatch(target):
        for fp in _served_pages(include_raw=True):
            if fp.stem == target:
                candidates.append(fp)
            else:
                # fallback by slugified title / basename
                try:
                    page = _page_from_path(fp)
                except Exception:
                    continue
                if _slugify(page.front.get("title", fp.stem)) == target:
                    candidates.append(fp)
    for fp in candidates:
        try:
            resolved = fp.resolve()
            resolved.relative_to(VAULT)
        except Exception:
            continue
        if fp.exists() and fp.suffix == ".md" and not _is_excluded(fp):
            page = _page_from_path(fp)
            if page.front.get("redirect"):
                return page
            if page.front.get("draft", "").lower() == "true" or page.front.get("status", "").lower() == "draft":
                return None
            return page
    return None


def _href_for_page(fp: Path) -> str:
    rel = str(fp.relative_to(VAULT)).replace(os.sep, "/")
    if rel == "index.md":
        return "/"
    return "/" + rel[:-3]


def _resolve_wikilink(target: str) -> str | None:
    page = _find(target)
    if page:
        return _href_for_page(page.path)
    return None


def _inline(text: str) -> str:
    """Render inline markdown. Escape first, then add only renderer-owned tags."""
    s = _h.escape(text)

    def repl_code(m: re.Match[str]) -> str:
        return f"<code>{m.group(1)}</code>"
    s = re.sub(r"`([^`]+)`", repl_code, s)

    def repl_wiki(m: re.Match[str]) -> str:
        target = _h.unescape(m.group(1)).strip()
        label = _h.unescape(m.group(2)).strip() if m.group(2) else target.split("/")[-1]
        href = _resolve_wikilink(target)
        if not href:
            return f'<span class="missing">{_h.escape(label)}</span>'
        return f'<a href="{_h.escape(href, quote=True)}">{_h.escape(label)}</a>'
    s = WIKILINK.sub(repl_wiki, s)

    def repl_mdlink(m: re.Match[str]) -> str:
        label = m.group(1)
        href = m.group(2)
        if ".." in href or not href.startswith("/"):
            return label
        return f'<a href="{_h.escape(href, quote=True)}">{label}</a>'
    s = MD_LINK.sub(repl_mdlink, s)

    def repl_src(m: re.Match[str]) -> str:
        raw_target = _h.unescape(m.group(1)).strip()
        href = _source_href(raw_target)
        if not href:
            return f'<sup class="src">source</sup>'
        return f'<sup class="src"><a href="{_h.escape(href, quote=True)}">источник</a></sup>'
    s = PROVENANCE.sub(repl_src, s)

    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def _split_table_row(line: str) -> list[str]:
    line = line.strip().strip("|")
    # Protect the display separator in [[slug|label]] from table splitting.
    protected = re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(0).replace("|", "\x00"), line)
    return [cell.strip().replace("\x00", "|") for cell in protected.split("|")]


def _render_body(body: str) -> str:
    out: list[str] = []
    para: list[str] = []
    ul: list[str] = []
    quote: list[str] = []
    table: list[list[str]] = []
    code: list[str] | None = None

    def flush_para() -> None:
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para.clear()

    def flush_ul() -> None:
        if ul:
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in ul) + "</ul>")
            ul.clear()

    def flush_quote() -> None:
        if quote:
            out.append("<blockquote>" + "<br>".join(_inline(x) for x in quote) + "</blockquote>")
            quote.clear()

    def flush_table() -> None:
        if table:
            rows = []
            for i, row in enumerate(table):
                tag = "th" if i == 0 else "td"
                rows.append("<tr>" + "".join(f"<{tag}>{_inline(c)}</{tag}>" for c in row) + "</tr>")
            out.append("<table>" + "".join(rows) + "</table>")
            table.clear()

    def flush_all() -> None:
        flush_para(); flush_ul(); flush_quote(); flush_table()

    for raw in body.splitlines():
        line = raw.rstrip("\n")
        if line.strip().startswith("```"):
            if code is None:
                flush_all()
                code = []
            else:
                out.append("<pre><code>" + _h.escape("\n".join(code)) + "</code></pre>")
                code = None
            continue
        if code is not None:
            code.append(line)
            continue
        stripped = line.strip()
        if not stripped:
            flush_para()
            continue
        m = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if m:
            flush_all()
            level = len(m.group(1))
            title = m.group(2).strip()
            out.append(f'<h{level} id="{_slugify(title)}">{_inline(title)}</h{level}>')
            continue
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
            if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
                continue
            flush_para(); flush_ul(); flush_quote()
            table.append(_split_table_row(stripped))
            continue
        if stripped.startswith("- "):
            flush_para(); flush_quote(); flush_table()
            ul.append(stripped[2:].strip())
            continue
        if stripped.startswith(">"):
            flush_para(); flush_ul(); flush_table()
            quote.append(stripped.lstrip(">").strip())
            continue
        flush_ul(); flush_quote(); flush_table()
        para.append(stripped)
    if code is not None:
        out.append("<pre><code>" + _h.escape("\n".join(code)) + "</code></pre>")
    flush_all()
    return "\n".join(out)


def _source_href(src: str) -> str | None:
    # Supports existing provenance like raw/articles/file.md and the requested
    # /sources/md/<slug>/<file>.md shape if pages later emit it.
    src = src.split("#", 1)[0].strip()
    if src.startswith("raw/") and src.endswith(".md"):
        return "/" + src[:-3]
    if src.startswith("sources/md/"):
        parts = src.split("/")
        if len(parts) == 4 and SLUG_OK.fullmatch(parts[2]) and FILE_OK.fullmatch(parts[3]):
            return "/" + src
    return None


def _resolve_source(parts: list[str]) -> Path | None:
    # /sources/md/<slug>/<file>.md -> raw/articles/<file>.md or raw/transcripts/<file>.md etc.
    if len(parts) != 4 or parts[0] != "sources" or parts[1] != "md":
        return None
    slug, filename = parts[2], parts[3]
    if not SLUG_OK.fullmatch(slug) or not FILE_OK.fullmatch(filename):
        return None
    for base in [VAULT / "raw" / "articles", VAULT / "raw" / "transcripts", VAULT / "raw" / "papers"]:
        target = base / filename
        try:
            target.resolve().relative_to(base.resolve())
        except Exception:
            continue
        if target.exists():
            return target
    return None


def _page_html(page: Page, public_base: str = "") -> str:
    title = page.front.get("title", "Home" if page.rel == "index.md" else page.path.stem)
    tags_html = ""
    tags = page.front.get("tags", "").strip("[]")
    if tags:
        tags_html = " ".join(f'<span class="tag">{_h.escape(t.strip())}</span>' for t in tags.split(",") if t.strip())
    mtime = datetime.fromtimestamp(page.path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    canonical = (public_base.rstrip("/") + _href_for_page(page.path)) if public_base else _href_for_page(page.path)
    nav = '<a href="/">🏠 Главная</a><a href="/_health">health</a>'
    body = _render_body(page.body)
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{_h.escape(title)} — Baza</title><style>{CSS}</style></head><body><nav class="nav">{nav}</nav><main class="container"><h1>{_h.escape(title)}</h1><div class="meta">{tags_html} modified: {mtime} · <a href="{_h.escape(canonical, quote=True)}">canonical</a></div>{body}</main></body></html>"""


class WikiHandler(BaseHTTPRequestHandler):
    server_version = "BazaWikiWeb/0.1"

    def log_message(self, format: str, *args: object) -> None:
        sys.stderr.write(f"{_now_msk()} {self.command} {self.path} {format % args}\n")

    def _send(self, code: int, body: str | bytes, content_type: str = "text/html; charset=utf-8") -> None:
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None: self._send(405, "read-only wiki", "text/plain; charset=utf-8")
    def do_PUT(self) -> None: self._send(405, "read-only wiki", "text/plain; charset=utf-8")
    def do_PATCH(self) -> None: self._send(405, "read-only wiki", "text/plain; charset=utf-8")
    def do_DELETE(self) -> None: self._send(405, "read-only wiki", "text/plain; charset=utf-8")

    def do_GET(self) -> None:
        try:
            self._handle_get()
        except Exception:
            traceback.print_exc()
            self._send(500, '<div class="err">Internal render error</div>')

    def _handle_get(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path).strip("/")
        if path == "_health":
            n = len(_served_pages(include_raw=False))
            self._send(200, f"ok pages={n}\n", "text/plain; charset=utf-8")
            return
        parts = path.split("/") if path else []
        if parts[:2] == ["sources", "md"]:
            src = _resolve_source(parts)
            if not src:
                self._send(404, "not found", "text/plain; charset=utf-8")
                return
            title = src.name
            body = "<pre><code>" + _h.escape(src.read_text(encoding="utf-8", errors="replace")) + "</code></pre>"
            self._send(200, f"<!doctype html><html lang='ru'><meta charset='utf-8'><style>{CSS}</style><main class='container'><h1>{_h.escape(title)}</h1>{body}</main></html>")
            return
        page = _find(path)
        if not page:
            self._send(404, "not found", "text/plain; charset=utf-8")
            return
        if page.front.get("redirect"):
            self.send_response(302)
            self.send_header("Location", _h.escape(page.front["redirect"], quote=True))
            self.end_headers()
            return
        public_base = getattr(self.server, "public_base", "")  # type: ignore[attr-defined]
        self._send(200, _page_html(page, public_base))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bind", default=os.environ.get("WIKI_WEB_BIND", "127.0.0.1"))
    ap.add_argument("--port", type=int, default=int(os.environ.get("WIKI_WEB_PORT", "8383")))
    ap.add_argument("--public-base", default=os.environ.get("WIKI_WEB_PUBLIC_BASE", ""))
    args = ap.parse_args()
    httpd = ThreadingHTTPServer((args.bind, args.port), WikiHandler)
    httpd.public_base = args.public_base  # type: ignore[attr-defined]
    print(f"Baza live wiki: http://{args.bind}:{args.port} vault={VAULT}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
