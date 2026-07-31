---
date: 2026-07-30
source: https://github.com/ragnor-rs/event-digest
tags: [telegram, ai, pipeline, events, typescript, clean-architecture]
---

# Event Digest CLI

AI-powered CLI tool для фильтрации Telegram сообщений через 7-шаговый pipeline и извлечения персонализированных анонсов мероприятий.

## Архитектура

**Clean Architecture + DDD:**

```
src/
├── domain/          # Бизнес-логика
│   ├── entities/    # DigestEvent, SourceMessage, InterestMatch
│   ├── interfaces/  # IAIClient, ICache, IMessageSource
│   └── services/    # Фильтрация, детекция, классификация
├── application/     # Оркестрация
│   └── event-pipeline.ts
├── data/           # Инфраструктура
│   ├── openai-client.ts
│   ├── telegram-client.ts
│   └── cache.ts
├── config/         # Конфигурация
└── presentation/   # Вывод
```

## 7-шаговый Pipeline

| Шаг | Сервис | Описание |
|-----|--------|----------|
| 1 | telegram-client | Загрузка сообщений из групп/каналов |
| 2 | event-cues-filter | Текстовая фильтрация по ключевым словам |
| 3 | event-detector | GPT детекция анонсов мероприятий |
| 4 | event-classifier | Классификация: offline/online/hybrid |
| 5 | schedule-matcher | Извлечение даты/времени + фильтр по слотам |
| 6 | interest-matcher | Матчинг с интересами + confidence scoring |
| 7 | event-describer | Генерация описаний (title, summary) |

## Ключевые паттерны

- **Incremental fetching** — `minId` параметр для загрузки только новых сообщений
- **Batch processing** — GPT запросы батчами для оптимизации затрат
- **Six-tier caching** — кэширование результатов GPT вызовов
- **Confidence scoring** — каждый шаг возвращает confidence 0.0-1.0

## Зависимости

- GramJS (Telegram Client API)
- OpenAI API (GPT для NLP)
- TypeScript + Node.js

## Применение для MCP Telegram

Pipeline можно реализовать поверх MCP Telegram инструментов:
- `mcp_telegram_get_dialogs` — получить список групп/каналов
- `mcp_telegram_get_messages` — загрузить сообщения
- GPT через имеющийся AI клиент

Вместо отдельного CLI — встроенный сценарий в Hermes.

## Конфиг

```yaml
groupsToParse:
  - "@example_tech_chat"
channelsToParse:
  - "@city_announcements"
userInterests:
  - "React development"
  - "Jazz concerts"
weeklyTimeslots:
  - "6 14:00"  # суббота 14:00
skipOnlineEvents: false
minInterestConfidence: 0.75
```

## Требования

- `TELEGRAM_API_ID` + `TELEGRAM_API_HASH` (my.telegram.org)
- `TELEGRAM_PHONE_NUMBER` (аккаунт для доступа)
- `OPENAI_API_KEY` (GPT запросы)

## Статус

Репозиторий: https://github.com/ragnor-rs/event-digest
Клон на сервере: `/home/ubuntu/event-digest` (мусор, удалить)

## Связанные заметки

- [[AI-ML/vibecoder-sources|Вайбкодерские источники]]
- [[AI-ML/asati-shill|Asati]]
- [[Projects/KPN-Agent/KPN-Agent|КПН-Агент]]
