---
source_url: https://github.com/3dstepansky (исследование Hermes, 2026-07-30)
ingested: 2026-07-30
sha256: 512dfe6778a4d4a2cdfec19205c27082ea999ac38df285a3cb493d68c89385d6
---

# OmniRoute: Исследование и Free-Tier Провайдеры 2026

**Дата исследования:** 30 июля 2026  
**Версия OmniRoute:** 3.8.49+  
**Endpoint:** http://127.0.0.1:20128/v1

---

## 1. Как добавить провайдера в OmniRoute

### Методы добавления провайдера

OmniRoute поддерживает три способа подключения провайдеров:

#### 1.1 Через Dashboard (Web UI)

```
Dashboard → Providers → Connect Provider
```

**Типы аутентификации:**
- **OAuth** — автоматический вход через провайдера (Claude Code, Gemini CLI, GitHub Copilot, etc.)
- **API Key** — ввод API ключа вручную
- **Web Cookie** — вставка cookie из браузера для веб-версий

#### 1.2 Через CLI

```bash
# Интерактивное добавление
omniroute provider add

# Тестирование подключения провайдера
omniroute provider test <provider-id>

# Пакетное тестирование всех провайдеров
omniroute providers test-batch

# Список подключённых провайдеров
omniroute provider list
```

#### 1.3 Через Environment Variables (Headless/CI)

```bash
# Пример для Docker/Kubernetes
export INITIAL_PASSWORD="your-secure-password"
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="AIza..."
export GROQ_API_KEY="gsk_..."

omniroute setup --non-interactive
```

### Формат конфигурации провайдера

Провайдеры определяются в `src/shared/constants/providers.ts` и хранятся в локальной SQLite базе.

**Структура провайдера:**

| Поле | Описание | Пример |
|------|----------|--------|
| `id` | Уникальный идентификатор | `nvidia`, `gemini`, `groq` |
| `alias` | Короткий псевдоним для моделей | `nv`, `gemini`, `groq` |
| `name` | Отображаемое имя | `NVIDIA NIM`, `Gemini (Google AI Studio)` |
| `tags` | Категории | `API key`, `OAuth`, `free`, `aggregator` |
| `website` | Ссылка на сайт | `https://build.nvidia.com` |
| `notes` | Заметки о free tier | `"Free dev access: ~40 RPM, 70+ models"` |

### Примеры добавления провайдеров

#### NVIDIA NIM (API Key)

```
Dashboard → Providers → Add Provider → NVIDIA NIM
- Provider ID: nvidia
- API Key: nvapi-xxxxx (получить на build.nvidia.com)
- Base URL: https://integrate.api.nvidia.com/v1 (автоматически)
```

**Модели:** `nvidia/glm-5.2`, `nvidia/deepseek-v4-flash`, `nvidia/qwen-2.5-72b-instruct`

#### Google Gemini (API Key)

```
Dashboard → Providers → Add Provider → Gemini
- Provider ID: gemini
- API Key: AIza... (получить на aistudio.google.com)
- Base URL: https://generativelanguage.googleapis.com/v1beta/openai (автоматически)
```

**Модели:** `gemini/gemini-2.5-flash`, `gemini/gemini-3.1-flash-lite`

#### Groq (API Key)

```
Dashboard → Providers → Add Provider → Groq
- Provider ID: groq
- API Key: gsk_... (получить на console.groq.com)
- Base URL: https://api.groq.com/openai/v1 (автоматически)
```

**Модели:** `groq/llama-3.1-8b-instant`, `groq/llama-3.3-70b-versatile`, `groq/qwen3-32b`

---

## 2. Актуальные Free-Tier Провайдеры 2026

### Сводная таблица

| Провайдер | Free Tier | Кредиты/Лимиты | Карта | Регистрация | Модели |
|-----------|-----------|----------------|-------|-------------|--------|
| **NVIDIA NIM** | ✅ Да | ~40 RPM, 70+ моделей | ❌ Нет | build.nvidia.com | GLM-5.2, DeepSeek V4, Kimi K2.6, Qwen |
| **Google AI Studio** | ✅ Да | 1,500 RPD (Flash), 50 RPD (2.5 Pro) | ❌ Нет | aistudio.google.com | Gemini 2.5 Flash, 3 Flash, 3.1 Flash-Lite |
| **Groq** | ✅ Да | 30 RPM, 14,400 RPD, 30K TPM | ❌ Нет | console.groq.com | Llama 3.1/3.3/4, Qwen3, DeepSeek R1 Distill |
| **DeepSeek** | ✅ Да | 5M токенов на регистрацию | ❌ Нет | platform.deepseek.com | DeepSeek V4 Flash/Pro, R1 |
| **OpenRouter** | ✅ Да | 20 RPM, 200 RPD на free модели | ❌ Нет | openrouter.ai | 15+ free моделей (Nemotron, Laguna, Ling) |
| **Cohere** | ✅ Да | 1,000 API calls/month | ❌ Нет | cohere.com | Command A+, Command R+, Rerank 3.5 |
| **Mistral** | ✅ Да | ~1B tokens/month, rate-limited | ❌ Нет | mistral.ai | Mistral Small/Medium/Large, Codestral |
| **Together AI** | ❌ Нет | $5 min purchase (было $25 credit) | ✅ Да | together.ai | Llama, Qwen, DeepSeek (paid only) |
| **Hugging Face** | ✅ Да | Free Inference API, rate-limited | ❌ Нет | huggingface.co | 45,000+ моделей (Whisper, SDXL, etc.) |
| **Cloudflare Workers AI** | ✅ Да | 10,000 Neurons/day | ❌ Нет | dash.cloudflare.com | Llama, Qwen, Mistral, Phi-2 |

---

## 3. Детальная информация по провайдерам

### 3.1 NVIDIA NIM (free-claude-code)

**Статус:** ✅ Free tier доступен

**Регистрация:**
1. Перейти на https://build.nvidia.com
2. Нажать "Get API Key"
3. Авторизоваться через NVIDIA аккаунт или Google/GitHub
4. API ключ генерируется автоматически

**Free Tier лимиты:**
- ~40 requests per minute (RPM)
- 70+ моделей бесплатно
- Нет expiry date для free tier
- Без кредитной карты

**Лучшие модели для кодинга:**
| Модель | Контекст | Назначение |
|--------|----------|------------|
| `glm-5.2` | 128K | Общий кодинг |
| `deepseek-v4-flash` | 1M | Быстрое программирование |
| `kimi-k2.6` | 256K | Сложные задачи |
| `qwen-2.5-72b-instruct` | 128K | Мультиязычный код |

**OmniRoute конфигурация:**
```json
{
  "provider": "nvidia",
  "apiKey": "nvapi-xxxxx",
  "models": ["nvidia/glm-5.2", "nvidia/deepseek-v4-flash"]
}
```

---

### 3.2 Google AI Studio (Gemini)

**Статус:** ✅ Free tier доступен (Flash модели)

**Регистрация:**
1. Перейти на https://aistudio.google.com
2. Войти через Google аккаунт
3. Нажать "Get API Key"
4. Создать новый API ключ

**Free Tier лимиты (апрель 2026):**
- **Gemini 2.5 Flash:** 1,500 RPD (requests per day)
- **Gemini 3 Flash:** 1,500 RPD
- **Gemini 3.1 Flash-Lite:** 1,500 RPD
- **Gemini 2.5 Pro:** 50 RPD (ограничено)
- **Pro модели:** Платные с 1 апреля 2026

**Требования:**
- ❌ Без кредитной карты
- ✅ Google аккаунт
- ⚠️ Данные используются для обучения (free tier)

**OmniRoute конфигурация:**
```json
{
  "provider": "gemini",
  "apiKey": "AIza...",
  "models": ["gemini/gemini-2.5-flash", "gemini/gemini-3-flash"]
}
```

---

### 3.3 Groq

**Статус:** ✅ Free tier доступен

**Регистрация:**
1. Перейти на https://console.groq.com
2. Sign up через Google/GitHub/email
3. API ключ создаётся сразу после регистрации

**Free Tier лимиты:**
| Метрика | Лимит |
|---------|-------|
| Requests per Minute (RPM) | 30 |
| Requests per Day (RPD) | 14,400 |
| Tokens per Minute (TPM) | 30,000 (зависит от модели) |
| Tokens per Day (TPD) | 500,000 |

**Лучшие модели:**
| Модель | TPM | TPS | Назначение |
|--------|-----|-----|------------|
| `llama-3.1-8b-instant` | 6K | 840 | Быстрые ответы |
| `llama-3.3-70b-versatile` | 12K | 394 | Сложные задачи |
| `llama-4-scout-17b` | 30K | 600 | Баланс |
| `qwen3-32b` | 6K | 500 | Мультиязычность |
| `deepseek-r1-distill-llama-70b` | — | — | Reasoning |

**Developer Tier (с картой):**
- 10x лимиты
- 25% скидка на токены
- Нет минимального платежа

**OmniRoute конфигурация:**
```json
{
  "provider": "groq",
  "apiKey": "gsk_...",
  "models": ["groq/llama-3.3-70b-versatile", "groq/qwen3-32b"]
}
```

---

### 3.4 DeepSeek

**Статус:** ✅ Free tier доступен

**Регистрация:**
1. Перейти на https://platform.deepseek.com
2. Sign up через email/Google/GitHub
3. Верификация email
4. API ключ в Dashboard

**Free Tier:**
- **5,000,000 токенов** на регистрацию
- Без кредитной карты
- Валидность: ~30 дней
- После: pay-as-you-go

**Цены (после free tier):**
| Модель | Input ($/1M) | Output ($/1M) | Cache Hit |
|--------|--------------|---------------|-----------|
| DeepSeek V4 Flash | $0.14 | $0.28 | $0.0028 |
| DeepSeek V4 Pro | $0.435 | $0.87 | $0.0036 |

**Контекст:** 1M tokens, 384K max output

**OmniRoute конфигурация:**
```json
{
  "provider": "deepseek",
  "apiKey": "sk-...",
  "models": ["deepseek/deepseek-chat", "deepseek/deepseek-reasoner"]
}
```

---

### 3.5 OpenRouter

**Статус:** ✅ Free models доступны

**Регистрация:**
1. Перейти на https://openrouter.ai
2. Sign up через Google/GitHub/email
3. API ключ генерируется автоматически

**Free Tier:**
- 20 RPM, 200 RPD на модели с суффиксом `:free`
- Без кредитной карты
- Каталог постоянно меняется

**Free модели (июль 2026):**
| Модель | Контекст | Назначение |
|--------|----------|------------|
| `nvidia/nemotron-3-ultra-550b:free` | 262K → 128K | Reasoning |
| `poolside/laguna-xs-2.1:free` | 256K | Coding agent |
| `inclusionai/ling-3.0-flash:free` | — | Multilingual |
| `qwen/qwen3-235b-a22b:free` | — | Large model |
| `deepseek/deepseek-r1:free` | — | Reasoning |

**⚠️ Важно:** Free модели могут быть удалены без предупреждения. За 9 дней до 27 июля 2026 удалено 7 free моделей (Llama, Qwen, Hermes).

**OmniRoute конфигурация:**
```json
{
  "provider": "openrouter",
  "apiKey": "sk-or-...",
  "models": [
    "openrouter/nvidia/nemotron-3-ultra-550b:free",
    "openrouter/poolside/laguna-xs-2.1:free"
  ]
}
```

---

### 3.6 Cohere

**Статус:** ✅ Free Trial API доступен

**Регистрация:**
1. Перейти на https://cohere.com
2. Sign up
3. Создать Trial API key

**Free Tier (Trial API Key):**
| Метрика | Лимит |
|---------|-------|
| API calls per month | 1,000 |
| Chat RPM | 20 |
| Embed RPM | 5 |

**Модели:**
- Command A+ (218B) — текст
- Command R+, Command R, Command R7B — RAG
- Rerank 3.5 — поиск
- Embed 4 — эмбеддинги
- Aya Expanse — мультиязычность

**Ограничения:**
- ❌ Только для тестирования/прототипов
- ❌ Не для коммерческого использования
- ✅ Без кредитной карты

**OmniRoute конфигурация:**
```json
{
  "provider": "cohere",
  "apiKey": "...",
  "models": ["cohere/command-a-plus-05-2026", "cohere/command-r-plus"]
}
```

---

### 3.7 Mistral AI

**Статус:** ✅ Free Experiment tier доступен

**Регистрация:**
1. Перейти на https://mistral.ai
2. Sign up на La Plateforme
3. SMS верификация (иногда)
4. API ключ создаётся автоматически

**Free Tier (Experiment):**
| Метрика | Лимит |
|---------|-------|
| Tokens per month | ~1,000,000,000 (1B) |
| Global rate limit | 1 req/sec per API key |
| Телефон | ✅ SMS верификация |
| Карта | ❌ Не требуется |

**Модели (все доступны):**
- Mistral Small
- Mistral Medium
- Mistral Large
- Codestral (кодинг)
- Mistral Embed

**Quota pools:**
| Модель | Tokens/min | Req/min | Tokens/month |
|--------|------------|---------|--------------|
| codestral-latest | 20,000 | 10 | 1,000,000,000 |
| mistral-large-latest | 20,000 | 10 | 1,000,000,000 |
| devstral-2512 | 1,000,000 | 50 | 10,000,000 |

**OmniRoute конфигурация:**
```json
{
  "provider": "mistral",
  "apiKey": "...",
  "models": ["mistral/mistral-large-latest", "mistral/codestral-latest"]
}
```

---

### 3.8 Together AI

**Статус:** ❌ Free tier отменён (июль 2025)

**Изменения:**
- Free trial credits **отменены** в июле 2025
- Минимальный депозит: **$5**
- Требуется кредитная карта

**Альтернативы:**
- Groq (бесплатно для Llama/Qwen)
- OpenRouter (free модели)
- NVIDIA NIM (бесплатно)

**Цены (paid):**
| Модель | Input ($/1M) | Output ($/1M) |
|--------|--------------|---------------|
| Llama 3.3 70B | $1.04 | $1.04 |
| DeepSeek V4 Pro | $2.10 | $4.40 |
| GLM-5.2 | $1.40 | $4.40 |

---

### 3.9 Hugging Face

**Статус:** ✅ Free Inference API доступен

**Регистрация:**
1. Перейти на https://huggingface.co
2. Sign up
3. Access Token в Settings → Access Tokens

**Free Tier:**
- Free Inference API для 45,000+ моделей
- Rate-limited (очереди)
- Без кредитной карты
- PRO аккаунт: $9/месяц (ускоренные очереди)

**Модели:**
- Whisper (speech-to-text)
- VITS (TTS)
- SDXL (images)
- Mistral, Llama, Qwen (text)
- Embedding модели

**OmniRoute конфигурация:**
```json
{
  "provider": "huggingface",
  "apiKey": "hf_...",
  "models": ["huggingface/mistral-7b-instruct"]
}
```

---

### 3.10 Cloudflare Workers AI

**Статус:** ✅ Free tier доступен

**Регистрация:**
1. Перейти на https://dash.cloudflare.com
2. Создать аккаунт
3. Workers AI → Get Started

**Free Tier (Workers Free):**
| Метрика | Лимит |
|---------|-------|
| Neurons per day | 10,000 |
| Reset | 00:00 UTC daily |
| После free tier | $0.011 per 1,000 Neurons |

**Rate Limits:**
| Task | RPM |
|------|-----|
| Text Generation | 300 |
| Text Embeddings | 3,000 |
| Image Classification | 3,000 |
| Speech Recognition | 720 |

**Модели:**
- `@cf/meta/llama-3.1-8b-instruct`
- `@cf/qwen/qwen1.5-14b-chat-awq`
- `@cf/mistral/mistral-7b-instruct-v0.1`
- `@cf/microsoft/phi-2`

**Требования:**
- Account ID (из dashboard)
- API Token (с правами Workers AI)

**OmniRoute конфигурация:**
```json
{
  "provider": "cloudflare-ai",
  "apiKey": "...",
  "accountId": "...",
  "models": ["cf/@cf/meta/llama-3.1-8b-instruct"]
}
```

---

## 4. Routing стратегии в OmniRoute

### 4.1 Типы стратегий

OmniRoute поддерживает **18 routing стратегий**:

| Стратегия | Описание |
|-----------|----------|
| **Priority** | Всегда первый в списке, fallback при ошибке |
| **Round-Robin** | Последовательная ротация |
| **Random** | Случайный выбор |
| **Weighted** | Пропорциональное распределение по весам |
| **Least-Used** | Минимальное количество запросов |
| **Cost-Optimized** | Самый дешёвый доступный |
| **Fusion** | Параллельные запросы к нескольким моделям |
| **Pipeline** | Последовательная обработка |

### 4.2 Auto-Routing

Самый простой способ — использовать модель `auto`:

```bash
# Автоматический выбор модели
curl http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -d '{"model": "auto", "messages": [...]}'
```

**Варианты auto:**
- `auto` — умный выбор
- `auto/coding` — оптимизация для кода
- `auto/fast` — минимальная latency
- `auto/cheap` — минимальная стоимость
- `auto/offline` — максимальный quota headroom

### 4.3 Combos (Fallback Chains)

Создание combo в Dashboard:

**Пример: Maximize Subscription + Free Backup**

```
Name: premium-with-free-fallback

Models:
1. cc/claude-opus-4-7 (Claude Pro subscription)
2. nvidia/glm-5.2 (NVIDIA free tier)
3. groq/llama-3.3-70b-versatile (Groq free tier)
4. gemini/gemini-2.5-flash (Google free tier)

Strategy: Priority
```

**Пример: Zero-Cost Combo**

```
Name: free-forever

Models:
1. gemini/gemini-2.5-flash (1,500 RPD free)
2. groq/llama-3.3-70b-versatile (14,400 RPD free)
3. openrouter/poolside/laguna-xs-2.1:free (200 RPD free)
4. nvidia/deepseek-v4-flash (40 RPM free)

Strategy: Round-Robin
```

### 4.4 CLI интеграция

**Claude Code:**
```bash
# Автонастройка
omniroute setup-claude-code

# Ручная настройка ~/.claude/config.json
{
  "anthropic_api_base": "http://localhost:20128/v1",
  "anthropic_api_key": "omniroute-api-key"
}
```

**Cursor:**
```json
// ~/.cursor/config.json
{
  "aiProvider": {
    "baseUrl": "http://localhost:20128/v1",
    "apiKey": "omniroute-api-key",
    "model": "auto/coding"
  }
}
```

**Codex CLI:**
```bash
export OPENAI_API_BASE="http://localhost:20128"
export OPENAI_API_KEY="omniroute-api-key"
```

---

## 5. Рекомендации по настройке

### 5.1 Для максимальной бесплатной работы

**Combo: Ultimate Free Stack**

```json
{
  "name": "ultimate-free",
  "models": [
    {"model": "gemini/gemini-2.5-flash", "priority": 1},
    {"model": "groq/llama-3.3-70b-versatile", "priority": 2},
    {"model": "nvidia/glm-5.2", "priority": 3},
    {"model": "mistral/codestral-latest", "priority": 4},
    {"model": "openrouter/poolside/laguna-xs-2.1:free", "priority": 5}
  ],
  "strategy": "priority"
}
```

**Ожидаемый ежедневный лимит:**
- Gemini: 1,500 запросов
- Groq: 14,400 запросов
- NVIDIA: ~57,600 запросов (40 RPM × 1440 min)
- Mistral: ~86,400 запросов (1 req/sec)
- OpenRouter: 200 запросов

**Итого: ~160,000+ запросов в день бесплатно**

### 5.2 Для кодинга

**Combo: Code Assistant**

```json
{
  "name": "code-assistant",
  "models": [
    {"model": "nvidia/glm-5.2", "priority": 1},
    {"model": "groq/llama-3.3-70b-versatile", "priority": 2},
    {"model": "deepseek/deepseek-chat", "priority": 3}
  ],
  "strategy": "auto/coding"
}
```

### 5.3 Для быстрого прототипирования

**Combo: Speed Demon**

```json
{
  "name": "speed-demon",
  "models": [
    {"model": "groq/llama-3.1-8b-instant", "priority": 1},
    {"model": "groq/llama-4-scout-17b", "priority": 2},
    {"model": "gemini/gemini-3-flash", "priority": 3}
  ],
  "strategy": "auto/fast"
}
```

---

## 6. Проверка работы OmniRoute

### 6.1 Health Check

```bash
# Проверка статуса
omniroute status

# Диагностика
omniroute doctor

# Список провайдеров
omniroute provider list
```

### 6.2 API Test

```bash
# Тест модели через OmniRoute
curl http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Hello, world!"}]
  }'
```

### 6.3 Dashboard

Открыть http://localhost:20128 в браузере для:
- Управления провайдерами
- Создания combos
- Мониторинга usage
- Настройки routing

---

## 7. Итоговая таблица регистрации

| Провайдер | URL регистрации | Где взять ключ | Карта | Free лимиты |
|-----------|-----------------|----------------|-------|-------------|
| **NVIDIA NIM** | build.nvidia.com | Get API Key → Copy | ❌ | 40 RPM, 70+ models |
| **Google AI Studio** | aistudio.google.com | Get API Key | ❌ | 1,500 RPD (Flash) |
| **Groq** | console.groq.com | API Keys → Create | ❌ | 30 RPM, 14.4K RPD |
| **DeepSeek** | platform.deepseek.com | API Keys | ❌ | 5M tokens |
| **OpenRouter** | openrouter.ai | Settings → Keys | ❌ | 20 RPM (free models) |
| **Cohere** | cohere.com | Trial API Key | ❌ | 1,000 calls/month |
| **Mistral** | console.mistral.ai | API Keys | ❌ | 1B tokens/month |
| **Hugging Face** | huggingface.co | Settings → Access Tokens | ❌ | Rate-limited |
| **Cloudflare** | dash.cloudflare.com | Workers AI → API Tokens | ❌ | 10K Neurons/day |

---

**Источник данных:** 
- OmniRoute Wiki (github.com/diegosouzapw/OmniRoute/wiki)
- Официальные сайты провайдеров
- PricePerToken.com
- Web search результаты (июль 2026)

**Подготовлено:** Hermes Agent Subagent  
**Дата:** 30 июля 2026
