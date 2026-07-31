---
source_url: https://github.com/3dstepansky (исследование Hermes, 2026-07-30)
ingested: 2026-07-30
sha256: 0603c4b1ed06893d0635b0d32f51e0eca7a15501056d2bd80fba75ebd851619f
---

# OmniRoute & Free Claude Code — Техническая документация

> Исследование GitHub репозиториев: OmniRoute, free-claude-code, omniroute-hybrid-setup

---

## 1. OmniRoute — Основной проект

### 1.1 Установка

```bash
# npm (рекомендуется)
npm install -g omniroute
omniroute

# Docker
docker run -p 20128:20128 diegosouzapw/omniroute

# Из исходников
git clone https://github.com/diegosouzapw/OmniRoute
cd OmniRoute
npm install
PORT=20128 DASHBOARD_PORT=20129 NEXT_PUBLIC_BASE_URL=http://localhost:20129 npm run dev
```

**Порты по умолчанию:**
- API: `http://localhost:20128/v1`
- Dashboard: `http://localhost:20128/dashboard`
- Split-port mode: API на 20128, Dashboard на 20129

### 1.2 Формат конфигурации провайдеров

OmniRoute не использует статический `config.yaml` для провайдеров. Конфигурация хранится в базе данных SQLite и управляется через:

1. **Dashboard UI** (`/dashboard/providers`)
2. **CLI команды** (`omniroute providers`)
3. **Environment переменные** для headless setup

#### Пример конфигурации через CLI

```bash
# Список доступных провайдеров
omniroute providers available

# Фильтрация по категории
omniroute providers available --category api-key
omniroute providers available --category oauth
omniroute providers available --category free
omniroute providers available --category local

# Категории: api-key, oauth, free, local, combo

# Добавить провайдер
omniroute provider add --id nvidia_nim --api-key nvapi-xxx

# Протестировать провайдер
omniroute providers test nvidia_nim

# Список сконфигурированных провайдеров
omniroute providers list --json
```

### 1.3 Переменные окружения

#### Базовые переменные

```bash
# Пароль администратора (headless setup)
INITIAL_PASSWORD="your-secure-password"
OMNIROUTE_PASSWORD="your-secure-password"

# Данные провайдеров
OMNIROUTE_API_KEY="sk-xxx"  # API ключ провайдера
OPENAI_API_KEY="sk-xxx"
ANTHROPIC_API_KEY="sk-xxx"
NVIDIA_NIM_API_KEY="nvapi-xxx"

# Директория данных
DATA_DIR="${HOME}/.local/share/omniroute"

# Порты
PORT=20128
DASHBOARD_PORT=20129
```

#### Timeout конфигурация

```bash
# Основные таймауты
REQUEST_TIMEOUT_MS=600000           # Базовый таймаут (10 минут)
STREAM_IDLE_TIMEOUT_MS=600000       # Макс. пауза между чанками в стриме

# Продвинутые переопределения
FETCH_TIMEOUT_MS=600000             # Таймаут до получения заголовков ответа
FETCH_HEADERS_TIMEOUT_MS=60000      # Undici timeout для заголовков
FETCH_BODY_TIMEOUT_MS=600000        # Undici timeout между чанками тела
FETCH_CONNECT_TIMEOUT_MS=30000      # TCP connect timeout
FETCH_KEEPALIVE_TIMEOUT_MS=4000     # Keep-alive socket timeout
```

#### Headless/CI setup

```bash
omniroute setup --non-interactive \
  --password "$OMNIROUTE_PASSWORD" \
  --api-key "$OPENAI_API_KEY" \
  --provider openai

omniroute providers test-batch
```

### 1.4 Routing стратегии

OmniRoute поддерживает **17+ routing стратегий**:

| Стратегия | Описание |
|-----------|----------|
| `auto` | Автоматический выбор на основе 9 факторов |
| `priority` | Приоритетный порядок |
| `weighted` | Взвешенное распределение |
| `fill-first` | Заполнение первого доступного |
| `round-robin` | Циклическое распределение |
| `least-used` | Наименее используемый |
| `cost-optimized` | Оптимизация по стоимости |
| `reset-aware` | Учет сброса квот |
| `reset-window` | Окно сброса квот |
| `headroom` | Запас по квоте |
| `strict-random` | Строгий случайный выбор |
| `lkgp` | Least Known Good Provider |
| `context-optimized` | Оптимизация контекста |
| `context-relay` | Relay с учетом контекста |
| `fusion` | Fan-out + judge synthesis (v3.8.36+) |
| `pipeline` | Последовательная обработка |

### 1.5 Combos (Fallback цепочки)

Combo — это именованный набор fallback-целей с routing стратегией.

#### Предустановленные combos

```
auto                  # Автоматический выбор (default combo)
auto/best-coding      # Лучший для кодинга
auto/best-fast        # Быстрые модели
auto/best-vision      # Vision модели
auto/best-reasoning   # Reasoning модели
auto/best-chat        # Чат модели
```

#### 4-tier auto-fallback

```
Tier 1: Subscription (Claude Code, Codex, Copilot)
    ↓ quota out
Tier 2: API Key (DeepSeek, Groq, xAI)
    ↓ budget hit
Tier 3: Cheap (GLM $0.5, MiniMax $0.2)
    ↓ budget hit
Tier 4: Free (Kiro, Qoder, Pollinations)
```

#### Пример использования combo

```bash
# В CLI инструменте
Base URL: http://localhost:20128/v1
API Key: sk-your-omniroute-key
Model: auto/best-coding
```

### 1.6 API Endpoints

| Endpoint | Описание |
|----------|----------|
| `/v1/chat/completions` | Standard chat (все провайдеры) |
| `/v1/responses` | Responses API (OpenAI format) |
| `/v1/completions` | Legacy text completions |
| `/v1/embeddings` | Text embeddings |
| `/v1/images/generations` | Image generation |
| `/v1/audio/speech` | Text-to-speech |
| `/v1/audio/transcriptions` | Speech-to-text |

#### Tokenized compatibility URLs

Для инструментов, не поддерживающих `Authorization` header:

```
Models:     http://localhost:20128/api/v1/vscode/YOUR_KEY/models
Chat:       http://localhost:20128/api/v1/vscode/YOUR_KEY/chat/completions
Responses:  http://localhost:20128/api/v1/vscode/YOUR_KEY/responses
Ollama:     http://localhost:20128/api/v1/vscode/YOUR_KEY/api/tags
Ollama chat: http://localhost:20128/api/v1/vscode/YOUR_KEY/api/chat
```

### 1.7 CLI команды

```bash
omniroute                    # Запуск сервера
omniroute setup              # Guided onboarding
omniroute doctor             # Диагностика без запуска сервера
omniroute providers          # Управление провайдерами
omniroute config             # Управление конфигурацией
omniroute status             # Offline status dashboard
omniroute logs               # Stream usage logs
omniroute update             # Проверка обновлений
omniroute --port 3000        # Кастомный порт
omniroute --mcp              # MCP server (stdio)
omniroute --no-open          # Не открывать браузер
```

#### Auto-configure для CLI инструментов

```bash
omniroute setup-codex        # ~/.codex/.config.toml
omniroute setup-claude       # ~/.claude/profiles/<profile>/settings.json
omniroute setup-opencode     # ~/.config/opencode/opencode.json
omniroute setup-cline        # VS Code extension settings
omniroute setup-kilo         # ~/.continue/config.yaml
omniroute setup-cursor       # Cursor settings
omniroute setup-aider        # ~/.aider.conf.yml
omniroute setup-goose        # ~/.config/goose/config.yaml
omniroute setup-qwen         # ~/.qwen/settings.json + ~/.qwen/.env
```

---

## 2. Free Claude Code

### 2.1 Установка

```bash
# macOS/Linux
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | bash

# Windows PowerShell
& ([scriptblock]::Create((Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.ps1").Content))
```

### 2.2 Запуск

```bash
# Linux
fcc-server

# Windows/macOS — Desktop launcher "Free Claude Code"

# Запуск Claude Code через FCC
fcc-claude

# Запуск Codex через FCC
fcc-codex

# Запуск Pi через FCC
fcc-pi
```

**Admin UI:** `http://127.0.0.1:8082/admin`

### 2.3 Настройка NVIDIA NIM

1. Создать API key на [build.nvidia.com/settings/api-keys](https://build.nvidia.com/settings/api-keys)
2. Открыть Admin UI
3. Вставить ключ в `NVIDIA_NIM_API_KEY`
4. Выбрать модель: `nvidia_nim/nvidia/nemotron-3-super-120b-a12b`
5. Нажать **Validate** → **Apply**

### 2.4 Переменные окружения

```bash
# Основные
NVIDIA_NIM_API_KEY="nvapi-xxx"     # NVIDIA NIM API ключ
HUGGINGFACE_API_KEY="hf_xxx"       # Для gated models

# Voice transcription
VOICE_BACKEND="nvidia_nim"          # или "cpu", "cuda"
WHISPER_MODEL="whisper-large-v3"
```

### 2.5 Интеграция с Telegram

FCC поддерживает интеграцию с Telegram для voice-note transcription:

```bash
# Установка с voice backend
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | bash -s -- --voice nvidia_nim
```

**Voice команды в Telegram:**
- `/stats` — Показать состояние сессии
- `/stop` — Отменить текущую работу
- `/clear` — Сбросить состояние FCC

### 2.6 Провайдеры (31+)

FCC поддерживает 31 cloud и local провайдер через Admin UI:

- NVIDIA NIM (FREE developer access — 70+ models)
- OpenAI
- Anthropic
- Google Gemini
- DeepSeek
- Groq
- xAI
- Mistral
- Local models (Ollama, vLLM)
- И другие

---

## 3. omniroute-hybrid-setup

### 3.1 Концепция

Local OmniRoute (Docker) как proxy перед cloud OmniRoute с fallback на local runtime модели.

```
Any client (OpenCode agent)
    ↓
localhost:20128 (Docker: omniroute container)
    ↓
best-* combo (priority routing)
    ↓
1. Cloud OmniRoute (auto/best-* model)
2. (fallback) Local runtime (host.docker.internal:11434/v1)
```

### 3.2 Конфигурация

#### Environment переменные (.env)

```bash
# Local OmniRoute
LOCAL_API_KEY="sk-local-xxx"
LOCAL_BASE_URL="http://127.0.0.1:20128"

# Cloud OmniRoute (upstream)
CLOUD_API_KEY="sk-cloud-xxx"
CLOUD_BASE_URL="https://your-cloud-omniroute.com"

# Local runtime (Ollama, vLLM)
LOCAL_RUNTIME_URL="http://host.docker.internal:11434/v1"
LOCAL_CODING="llama3.2:latest"
LOCAL_FAST="llama3.2:latest"
LOCAL_REASONING="deepseek-r1:8b"
LOCAL_VISION="llava:latest"
```

### 3.3 Combos

Скрипт создаёт priority combos с cloud primary + local fallback:

| Combo | Cloud model | Fallback |
|-------|-------------|----------|
| `best-coding` | `auto/best-coding` | `LOCAL_CODING` |
| `best-coding-fast` | `auto/best-coding-fast` | `LOCAL_CODING` |
| `best-fast` | `auto/best-fast` | `LOCAL_FAST` |
| `best-vision` | `auto/best-vision` | `LOCAL_VISION` |
| `best-reasoning` | `auto/best-reasoning` | `LOCAL_REASONING` |
| `best-chat` | `auto/best-chat` | `LOCAL_REASONING` |

### 3.4 Интеграция с OpenCode

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "omniroute/best-coding",
  "small_model": "omniroute/best-fast",
  "provider": {
    "omniroute": {
      "options": {
        "baseUrl": "http://127.0.0.1:20128",
        "apiKey": "${OMNIROUTE_LOCAL_API_KEY}"
      }
    }
  }
}
```

### 3.5 Запуск

```bash
# Требования
# - uv (Python package manager)
# - Docker compose v2
# - Local runtime (Ollama с моделями)

cp .env.example .env
# Отредактировать .env

make up  # или docker compose up -d
```

---

## 4. Примеры конфигурации для CLI инструментов

### 4.1 Claude Code

```bash
# ~/.claude/profiles/default/settings.json
{
  "apiProvider": "openai-compatible",
  "openaiCompatible": {
    "baseUrl": "http://localhost:20128/v1",
    "apiKey": "sk-your-omniroute-key"
  }
}

# Или через launcher
omniroute launch
```

### 4.2 Codex CLI

```bash
# ~/.codex/.config.toml
[profiles.omniroute]
api_base = "http://localhost:20128/v1"
api_key = "sk-your-omniroute-key"

# Или через launcher
omniroute launch-codex
```

### 4.3 OpenCode

```json
// ~/.config/opencode/opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "omniroute": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "OmniRoute",
      "options": {
        "baseURL": "http://localhost:20128/v1",
        "apiKey": "sk-your-omniroute-key"
      },
      "models": {
        "claude-sonnet-4-5": { "name": "claude-sonnet-4-5" },
        "gemini-3-flash": { "name": "gemini-3-flash" }
      }
    }
  }
}
```

### 4.4 Continue.dev

```yaml
# ~/.continue/config.yaml
models:
  - name: OmniRoute
    provider: openai
    model: auto
    apiBase: http://localhost:20128/v1
    apiKey: sk-your-omniroute-key
    default: true
```

### 4.5 Cline / Kilo Code / Roo Code

```bash
# VS Code settings.json
{
  "kilo-code.openAiBaseUrl": "http://localhost:20128/v1",
  "kilo-code.apiKey": "sk-your-omniroute-key"
}

# Или CLI
kilocode --api-base http://localhost:20128/v1 --api-key sk-your-omniroute-key
```

### 4.6 Cursor

Через dashboard: `omniroute setup-cursor` — выводит инструкции для in-app настройки.

---

## 5. MCP (Model Context Protocol)

### 5.1 Запуск MCP server

```bash
# stdio mode
omniroute --mcp

# HTTP MCP endpoint
http://localhost:20128/api/mcp/stream
```

### 5.2 Конфигурация MCP клиента

**Claude Code:**
```bash
claude mcp add-server omniroute \
  --type http \
  --url http://localhost:20128/api/mcp/stream
```

**Cursor / Cline:**
```json
{
  "mcpServers": {
    "omniroute": {
      "command": "omniroute",
      "args": ["--mcp"],
      "env": {}
    }
  }
}
```

**MCP tools:** 104 built-in tools для управления gateway, routing, providers, combos, cache, compression, memory.

---

## 6. A2A (Agent-to-Agent Protocol)

### 6.1 Agent Card

```bash
curl http://localhost:20128/.well-known/agent.json
```

### 6.2 Пример запроса

```bash
curl -X POST http://localhost:20128/api/a2a \
  -H 'content-type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "quickstart",
    "method": "message/send",
    "params": {
      "skill": "quota-management",
      "messages": [{"role": "user", "content": "Give me a short quota summary."}]
    }
  }'
```

---

## 7. Docker Compose пример

```yaml
# compose.yml
version: "3.9"

services:
  omniroute:
    image: diegosouzapw/omniroute:latest
    ports:
      - "20128:20128"
    environment:
      - PORT=20128
      - INITIAL_PASSWORD=${OMNIROUTE_PASSWORD}
      - DATA_DIR=/data
    volumes:
      - omniroute-data:/data
    restart: unless-stopped

volumes:
  omniroute-data:
```

---

## 8. Связанные проекты

### 8.1 VansRouter
- URL: https://github.com/Vanszs/VansRouter
- Описание: Lightweight Version of 9Route x Omniroute Combined Logic
- Stars: 152

### 8.2 OmniGlyph
- URL: https://github.com/diegosouzapw/OmniGlyph
- Описание: Cut Claude bill 59–70% by rendering LLM context as PNG pages
- Stars: 55

### 8.3 GH_OmniRout
- URL: https://github.com/oxo-xux/GH_OmniRout
- Описание: GitHub Actions Runner + Cloudflare Tunnel для OmniRoute
- Stars: 2

### 8.4 self-hosted-OmniRoute
- URL: https://github.com/Cognivanta-AI/self-hosted-OmniRoute
- Описание: Coolify-ready deployment template with Docker Compose

### 8.5 omniroute-sdk
- URL: https://github.com/azazelpy/omniroute-sdk
- Описание: Multi-provider LLM gateway SDK (TS/Python/Go)

---

## 9. Ключевые особенности OmniRoute

- **268 провайдеров** — наибольший каталог среди open-source gateway
- **90+ free tiers** — автоматическое использование free квот
- **17 routing стратегий** — гибкая маршрутизация
- **4-tier auto-fallback** — всегда онлайн
- **RTK + Caveman compression** — экономия 15-95% токенов
- **104 MCP tools** — управление gateway через MCP
- **A2A protocol** — agent-to-agent взаимодействие
- **25,000+ tests** — production-ready
- **Memory** — FTS5 + Qdrant vector recall
- **Circuit breakers** — отказоустойчивость
- **TLS stealth** — обход блокировок

---

## Ссылки

- **OmniRoute:** https://github.com/diegosouzapw/OmniRoute
- **Website:** https://omniroute.online
- **npm:** https://npmjs.com/package/omniroute
- **Docker Hub:** https://hub.docker.com/r/diegosouzapw/omniroute
- **Free Claude Code:** https://github.com/Alishahryar1/free-claude-code
- **omniroute-hybrid-setup:** https://github.com/disafronov/omniroute-hybrid-setup
