import importlib.util
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from subprocess import Popen, PIPE
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("wiki_web", ROOT / "scripts" / "wiki_web.py")
assert SPEC is not None and SPEC.loader is not None
wiki_web = importlib.util.module_from_spec(SPEC)
sys.modules["wiki_web"] = wiki_web
SPEC.loader.exec_module(wiki_web)


def test_inline_escapes_html_and_renders_own_links():
    html = wiki_web._inline("<script>alert(1)</script> **bold** `x`")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "<strong>bold</strong>" in html
    assert "<code>x</code>" in html


def test_table_split_protects_wikilink_pipe():
    row = wiki_web._split_table_row("| [[entities/green-broker|Green Broker]] | ok |")
    assert row == ["[[entities/green-broker|Green Broker]]", "ok"]


def test_render_broken_wikilink_as_plain_missing_text():
    html = wiki_web._inline("[[definitely-no-such-page|Missing Page]]")
    assert '<a href=' not in html
    assert 'class="missing"' in html
    assert "Missing Page" in html


def _free_port():
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def test_http_routes_health_page_405_and_traversal():
    port = _free_port()
    proc = Popen(
        [sys.executable, str(ROOT / "scripts" / "wiki_web.py"), "--bind", "127.0.0.1", "--port", str(port)],
        cwd=str(ROOT), stdout=PIPE, stderr=PIPE, text=True,
    )
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(30):
            try:
                txt = urllib.request.urlopen(base + "/_health", timeout=1).read().decode()
                if txt.startswith("ok pages="):
                    break
            except Exception:
                time.sleep(0.1)
        else:
            raise AssertionError("server did not start")
        page = urllib.request.urlopen(base + "/construction-maps-mcp", timeout=3).read().decode()
        assert "Construction Maps MCP" in page
        assert "Контекст для Green Broker" in page
        try:
            urllib.request.urlopen(urllib.request.Request(base + "/", method="POST"), timeout=3)
        except urllib.error.HTTPError as e:
            assert e.code == 405
        else:
            raise AssertionError("POST should be 405")
        try:
            urllib.request.urlopen(base + "/../SCHEMA", timeout=3)
        except urllib.error.HTTPError as e:
            assert e.code == 404
        else:
            raise AssertionError("traversal should be 404")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
