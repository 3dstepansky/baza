---
date: 2026-07-30
source: github
tags: [llm, proxy, gateway, ai, free-tier, omniroute]
---

# OmniRoute

**GitHub:** https://github.com/topics/omniroute
**Версия:** v3.8.49 (23.6K ⭐)

## Описание

Бесплатный локальный AI-прокси для LLM с поддержкой:
- **271 провайдер** (90+ с free tier, 40+ free forever)
- **18 routing стратегий** (strict-random, round-robin, etc.)
- **Compression pipeline** (RTK + Caveman, 15-95% экономия токенов)
- **Quota-Share** — разделение квоты между командой

## Архитектура

```
Cursor/Codex/Claude Code
       ↓
  Compression Layer
       ↓
   OmniRoute Gateway (localhost:20128)
       ↓
  271 Provider Pool
```

## Ключевые фичи

- **Бесплатные провайдеры:** Gemini, DeepSeek, Cohere, Mistral, xAI
- **Token compression:** PNG pages, Session-Dedup, CCR
- **Local-first:** все ключи хранятся локально
- **OAuth интеграция:** Zed IDE, Cursor, Claude Code

## Использование

Уже настроен на сервере как `custom:omniroute`:
- Endpoint: `http://127.0.0.1:20128/v1`
- Модель: `deepseek-web/deepseek-v4-flash`

## Инсайды для мониторинга

- Новые free-tier провайдеры
- Изменения в rate limits
- Обновления compression алгоритмов
- Интеграции с новыми IDE

## Связанные проекты

- `omniroute-gh-runner` — GitHub Actions deployment
- `omniroute-hybrid-setup` — hybrid local/cloud
