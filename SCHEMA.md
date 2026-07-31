# Wiki Schema — Baza (LLM Wiki)

> Управляющий документ базы знаний. Читать ПЕРЕД любой операцией в новой сессии
> (вместе с `index.md` и `log.md`). Методология: Karpathy's LLM Wiki (скилл `llm-wiki` v2.1.0).

## Domain

Персональная база знаний Павла: AI/ML, вайбкодинг, разработка, алготрейдинг,
инфраструктура Hermes, проекты (КПН-Агент, Telemost Recorder, Marketplace),
холдинг «Синергия».

## Расположение

- Vault: `/home/ubuntu/baza` (Obsidian, MCP-сервер `baza`)
- Публикация: `_site/` (build-site.py) + `vault-graph.html` (generate-graph.py)
- Git: https://github.com/3dstepansky/baza

## Структура

```
baza/
├── SCHEMA.md            # этот файл
├── index.md             # корневой хаб (разделы)
├── log.md               # журнал действий (append-only, ротация на 500 записей)
├── Dev/                 # разработка, языки
├── AI-ML/               # модели, MCP, free-tier, источники
├── Trading/             # алготрейдинг
├── System/              # серверы, Hermes
├── Concepts/            # концепции (Karpathy-style)
├── Projects/            # активные проекты
├── Synergy/             # холдинг «Синергия»
└── raw/                 # Layer 1: неизменяемые источники (по мере появления)
```

## Conventions

- Имена файлов: `Kebab-Case.md` / `Title-Case.md`, без пробелов
- Каждая заметка начинается с YAML frontmatter: `date`, `tags`
- `[[wikilinks]]` между страницами: **минимум 2 исходящие ссылки** на страницу
- При обновлении страницы — обновлять `date`
- Каждая новая страница добавляется в `index.md` (или хаб раздела) в нужную секцию
- Каждое действие записывается в `log.md`
- **Provenance:** на страницах, синтезирующих 3+ источника, помечать абзацы `^[source]`
- **Confidence:** `confidence: high|medium|low` для спорных/быстро меняющихся тем

## Frontmatter

```yaml
---
date: YYYY-MM-DD
tags: [из таксономии]
confidence: medium        # опционально: high|medium|low
contested: true           # опционально: есть противоречия
sources: [ссылка]         # опционально
---
```

## Tag Taxonomy

Разделённые теги (добавлять новые ТОЛЬКО через этот список):

- **AI/ML**: ai, llm, mcp, free-tier, model, local-llm, omniroute, whisper
- **Разработка**: dev, python, go, node, docker, n8n
- **Проекты**: project, kpn-agent, telemost, marketplace, wb, ozon
- **Инфраструктура**: system, hermes, server, proxy, telegram
- **Трейдинг**: trading, algo
- **Знания**: concept, wiki, obsidian, source, monitoring
- **Холдинг**: synergy, org-structure, meeting

## Page Thresholds

- **Создавать страницу**: сущность/концепция в 2+ источниках ИЛИ центральная для одного
- **Дополнять существующую**: источник упоминает уже покрытое
- **НЕ создавать**: проходные упоминания, мелочи, вне домена
- **Сплит страницы**: >200 строк — разбить с перекрёстными ссылками
- **Архив**: контент полностью замещён → `_archive/`, убрать из index

## Update Policy

1. Свежие источники обычно заменяют старые (проверять даты)
2. При противоречии — фиксировать обе позиции с датами и источниками
3. Помечать `contested: true` / `contradictions: [page]`
4. Выносить на ревью пользователя в lint-отчёте
