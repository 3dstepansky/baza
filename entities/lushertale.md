---
title: LusherTale / ПсихоСказка
type: entity
created: 2026-08-17
updated: 2026-08-17
tags: [project, bot, telegram, python, docker, ai, llm, api, github, yougile, notebooklm]
sources: [raw/articles/lushertale-project-context-2026-08-17.md]
confidence: high
---

# LusherTale / ПсихоСказка

**LusherTale / ПсихоСказка** — Telegram-бот для генерации терапевтических сказок-метафор на основе цветового теста Люшера. Проект развёрнут как отдельный Docker-сервис и не является частью Hermes, но Hermes используется как рабочий агент для деплоя, настройки, интеграций и ведения базы знаний.

## Быстрые факты

| Поле | Значение |
|---|---|
| Название | LusherTale / ПсихоСказка |
| Telegram bot | `@Lush123Bot` |
| Репозиторий | https://github.com/aaulitina77-spec/LusherTale |
| Серверная директория | `/home/ubuntu/LusherTale` |
| Docker compose project | `psyhoskazka` |
| Контейнер | `psyhoskazka-bot-1` |
| Статус на 2026-08-17 | контейнер был проверен как `Up 2 days` |
| Основной лидер проекта | [[entities/nastya-wkrmst|Настя / @Wkrmst]] |
| YouGile project | `психосказка фичи` |

## Продуктовая суть

Пользователь проходит 2 круга выбора 8 цветов. Бот строит профиль по правилам Люшера, берёт интерпретации из базы и генерирует сказку как мягкую метафору психологического состояния.

Целевая логика продукта:

1. пользователь открывает Telegram-бота;
2. проходит WebApp-тест Люшера;
3. бот анализирует последовательности цветов;
4. AI генерирует терапевтическую сказку;
5. пользователь оценивает сказку через NPS;
6. баланс пополняется через Telegram Stars.

## Архитектура

| Слой | Реализация |
|---|---|
| Telegram bot | Python 3.12, aiogram 3.16 |
| WebApp | HTML/CSS/JS, тест Люшера |
| DB | SQLite, volume `bot_data` |
| AI | OpenAI-compatible API через `bot/python/services/openrouter.py` |
| Deploy | Docker Compose |
| Payments | Telegram Stars |
| Admin | `/admin`, NPS, аналитика, feedback |

Ключевые файлы проекта:

- `/home/ubuntu/LusherTale/README.md` — актуальный README;
- `/home/ubuntu/LusherTale/ARCHITECTURE.md` — Mermaid-схемы архитектуры, сценария, ER и оплаты;
- `/home/ubuntu/LusherTale/AGENTS.md` — команды и контекст для агентов;
- `bot/python/services/luscher.py` — ядро анализа Люшера;
- `bot/python/services/openrouter.py` — AI-генерация сказок;
- `database/seed_luscher_rules_sqlite.sql` — 286 интерпретаций PsyLab.

## AI / OmniRoute context

Павел отдельно просил подключать генерацию сказок к OpenAI-compatible API через существующий агентский/OmniRoute-контур, а не оставлять только заглушку. Это связывает проект с [[entities/omniroute|OmniRoute]] и общим слоем AI gateway.

Практическая рамка:

- использовать OpenAI-compatible endpoint;
- не хранить секреты в wiki;
- модель и base URL фиксировать в `.env` проекта, не в тексте заметки;
- проверять реальную генерацию сказки после смены модели.

## YouGile / управление фичами

YouGile подключён к Hermes через MCP-сервер `yougile` на пакете `@nebelov/yougile-mcp`.

| Поле | Значение |
|---|---|
| Company | `AIBots` |
| Company ID | `e585f7f5-0144-4955-b859-754e78aa5c11` |
| Project | `психосказка фичи` |
| Project ID | `191f45b9-7a1b-4947-9d32-3701cfd0ecf4` |
| Boards | `Фичи`, `Сократить длину и стиль` |

Секреты — `YOUGILE_API_KEY`, логин/пароль — в базе знаний не хранить. Если MCP tools отвечают `Not authorized`, но прямой API с сохранённым ключом работает, вероятная причина — stale env текущей сессии; нужен `/new` или рестарт gateway.

## NotebookLM links

NotebookLM связан с этим проектом как слой презентации/артефактов:

| Артефакт | Ссылка / путь | Статус |
|---|---|---|
| NotebookLM notebook | https://notebook.google.com/notebook/37e16902-bd53-4852-ae9d-badd7116d4ca | проектный блокнот LusherTale |
| Инфографика | «ПсихоСказка: от цвета к метафоре» | создана в NotebookLM |
| Verified PNG | `/home/ubuntu/notebooklm-lushertale-podcast/infographic/real/ПсихоСказка__от_цвета_к_метафоре.png` | `PNG image data, 2752 x 1536`, 4.3 MB |

Правило качества: NotebookLM-артефакт считается готовым только после проверки MIME/magic bytes (`file`, `ffprobe` для аудио). UI-скриншот не равен экспортированной инфографике.

## Роли и коммуникации

- [[entities/nastya-wkrmst|Настя / @Wkrmst]] — лидер проекта со сказками по Люшеру.
- Связь с Настей вести через [[concepts/mcp|Telegram MCP]] только когда Павел явно просит написать/отправить сообщение.
- Павел не хочет, чтобы сообщения Насте отправлялись без явной команды.

## Связанные страницы

- [[entities/nastya-wkrmst|Настя / @Wkrmst]]
- [[entities/omniroute|OmniRoute]]
- [[concepts/mcp|MCP — Model Context Protocol]]
- [[entities/hermes-agent|Hermes Agent]]
- [[raw/articles/lushertale-project-context-2026-08-17|Raw context: LusherTale]]
