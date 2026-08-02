# Wiki Schema

> Управляющий документ. Читать ПЕРВЫМ в новой сессии вместе с index.md и log.md.
> Методология: Karpathy's LLM Wiki (скилл llm-wiki v2.1.0). WIKI_PATH=/home/ubuntu/baza

## Domain

Персональная база знаний: AI/ML и вайбкодинг, free-tier провайдеры, разработка,
алготрейдинг, инфраструктура Hermes, проекты (КПН-Агент, Telemost Recorder),
холдинг «Синергия».

## Структура (три слоя)

```
baza/
├── SCHEMA.md            # этот файл
├── index.md             # КАТАЛОГ всех страниц (единственный index.md!)
├── log.md               # журнал действий (append-only)
├── raw/                 # Layer 1: ИММУТАБЕЛЬНЫЕ источники (не редактировать!)
│   ├── articles/        #   статьи, отчёты
│   ├── papers/          #   PDF, arxiv
│   ├── transcripts/     #   расшифровки встреч
│   └── assets/          #   изображения
├── entities/            # Layer 2: сущности (люди, орг., продукты, модели)
├── concepts/            # Layer 2: концепции/темы
├── comparisons/         # Layer 2: сравнения
├── queries/             # Layer 2: сохранённые ценные ответы
└── _archive/            # замещённые/хабы
```

## Conventions

- Имена файлов: lowercase, hyphens, без пробелов (например `telemost-recorder.md`)
- Каждая страница начинается с YAML frontmatter (см. ниже)
- `wikilinks` — минимум 2 исходящие ссылки на страницу
- При обновлении страницы — бампить `updated`
- Каждая новая страница добавляется в `index.md` в нужную секцию
- Каждое действие записывается в `log.md`
- **Provenance:** на страницах, синтезирующих 3+ источника, помечать абзацы `^[raw/articles/file.md]`
- **ВАЖНО: в vault только ОДИН index.md — корневой каталог.** Хабы не нужны — навигация через index.md
- **raw/ никогда не редактировать** — исправления только в wiki-страницах

## Frontmatter

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [из таксономии]
sources: [raw/articles/source.md]
confidence: high | medium | low   # опционально
contested: true                   # опционально
---
```

## Tag Taxonomy

Правило: тег должен быть в таксономии; новые теги — сначала сюда.

- **Типы страниц**: entity, concept, comparison, query
- **AI/ML**: llm, mcp, model, free-tier, local-llm, whisper, omniroute, openrouter, groq
- **Продукты/Организации**: product, project, org, tool, bot, channel, job-search
- **Техники**: agent, protocol, rag, trading, automation, scraping, multi-agent, orchestration, methodology, benchmark, quality-gate, spec-driven, security
- **Стек**: python, go, node, docker, telegram, obsidian, github, claude-code, codex
- **Данные/Мета**: meeting, transcript, monitoring, wiki, halyava

## Page Thresholds

- **Создавать страницу**: сущность/концепция в 2+ источниках ИЛИ центральная для одного
- **Дополнять существующую**: источник упоминает уже покрытое
- **НЕ создавать**: проходные упоминания, мелочи, вне домена
- **Сплит**: страница >200 строк — разбить с перекрёстными ссылками
- **Архив**: контент полностью замещён → `_archive/`, убрать из index

## Типы страниц

- **Entity** — одна страница на сущность: обзор, ключевые факты, связи (wikilinks), источники
- **Concept** — определение, текущее состояние, открытые вопросы, связанные концепции
- **Comparison** — что сравнивается и зачем, измерения (таблица), вердикт, источники
- **Query** — сохранённый ответ, который больно пере-выводить

## Update Policy

1. Свежие источники обычно заменяют старые (проверять даты)
2. При противоречии — фиксировать обе позиции с датами и источниками
3. Помечать `contested: true` / `contradictions: [page]`
4. Выносить на ревью в lint-отчёте
