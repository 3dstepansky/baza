---
title: "Free-tier LLM провайдеры: сравнение 2026"
created: 2026-07-31
updated: 2026-07-31
type: comparison
tags: [free-tier, llm, comparison, halyava]
sources: [raw/articles/omniroute-free-tier-providers-report.md]
confidence: medium
---

# Free-tier LLM провайдеры — сравнение

**Что сравнивается:** бесплатные tier'ы LLM-провайдеров для zero-cost работы агентов.
**Зачем:** выбрать провайдеров под [[concepts/free-ai-methods|методы бесплатного доступа]] без карты.

## Сравнительная таблица

| Провайдер | Free tier | Лимиты | Карта | Регистрация |
|-----------|-----------|--------|-------|-------------|
| NVIDIA NIM | ✅ | ~40 RPM, 70+ моделей | ❌ | build.nvidia.com |
| Google AI Studio | ✅ | 1500 RPD (Flash) | ❌ | aistudio.google.com |
| Groq | ✅ | 30 RPM, 14.4K RPD | ❌ | console.groq.com |
| DeepSeek | ✅ | 5M токенов на старт | ❌ | platform.deepseek.com |
| OpenRouter | ✅ | 20 RPM, 200 RPD free | ❌ | openrouter.ai |
| Cohere | ✅ | 1000 calls/мес | ❌ | cohere.com |
| Mistral | ✅ | ~1B ток/мес, rate-limited | ❌ | mistral.ai |
| Cloudflare Workers AI | ✅ | 10K нейронов/день | ❌ | dash.cloudflare.com |
| Together AI | ❌ | $5 min purchase | ✅ | together.ai |

## Вердикт

- **Без карты и навсегда:** NVIDIA NIM, Google AI Studio, Groq, Cloudflare — топ для [[entities/omniroute|OmniRoute]] и free-claude-code
- **Для кодинга:** NVIDIA NIM (free-claude-code, 40 RPM)
- **Для быстрых прототипов:** Groq (скорость), Google AI Studio (1500 RPD)
- **DeepSeek** — 5M токенов разово + дешёвые paid тарифы

## Связанные страницы

- [[entities/omniroute|OmniRoute]]
- [[concepts/free-ai-methods|Методы бесплатного доступа]]
- [[concepts/llm-wiki|LLM Wiki]]
