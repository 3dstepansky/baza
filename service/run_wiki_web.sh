#!/usr/bin/env bash
set -euo pipefail
cd /home/ubuntu/baza
export WIKI_PATH=/home/ubuntu/baza
export WIKI_WEB_BIND="${WIKI_WEB_BIND:-0.0.0.0}"
export WIKI_WEB_PORT="${WIKI_WEB_PORT:-8383}"
export WIKI_WEB_PUBLIC_BASE="${WIKI_WEB_PUBLIC_BASE:-http://127.0.0.1:8383}"
exec python3 scripts/wiki_web.py --bind "$WIKI_WEB_BIND" --port "$WIKI_WEB_PORT" --public-base "$WIKI_WEB_PUBLIC_BASE"
