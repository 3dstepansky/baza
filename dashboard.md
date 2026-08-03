---
title: LLM Wiki Baza Dashboard
created: 2026-08-03
updated: 2026-08-03
type: query
tags: [wiki, dashboard, lint]
sources: []
confidence: high
---

# 📖 LLM Wiki Baza Dashboard

> Панель состояния базы знаний Павла. Обновлено: **2026-08-03 09:00 UTC**.

<div class="button-grid">
<a class="button" href="index.html">🏠 Главная база</a>
<a class="button" href="vault-graph.html">🕸️ Граф связности</a>
<a class="button" href="entities/telemost-recorder.html">📹 Telemost Recorder</a>
<a class="button" href="entities/green-broker.html">🌿 Green Broker</a>
<a class="button" href="log.html">🧾 Журнал ведения</a>
<a class="button" href="https://github.com/3dstepansky/baza">GitHub repo</a>
</div>

## Состояние

- Markdown-файлов в vault: **74**
- Wiki-страниц без raw/_archive: **45**
- Последний git commit: `d31d768 Update Telemost Recorder project knowledge`
- Ветка: `main`

## Lint / связность

Методологический быстрый lint считает wiki-слой, исключает `raw/`, `_archive/` и примеры `[[...]]` внутри code-блоков.

- Broken wikilinks: **0**
- Orphans: **1**
- Low outbound pages <2 links: **1**

## Актуальные добавления

- [[entities/telemost-recorder|Telemost Recorder]] — проект по Телемосту, актуальная ветка `v04`, архитектура и тесты зафиксированы.
- [[entities/green-broker|Green Broker]] — реальный проект Павла, внесены constitution/spec/plan и КП PDF.
- [[concepts/multi-agent-development-methodology|Multi-agent development methodology]] — методология многоагентной разработки.
- [[concepts/spec-driven-agent-development|Spec-driven agent development]] — Constitution → Spec → Plan → Tasks → Implement.

## Как ведётся база

- `raw/` — неизменяемые источники.
- `entities/`, `concepts/`, `comparisons/`, `queries/` — смысловой wiki-слой.
- [[index|index.md]] — каталог всех страниц.
- [[log|log.md]] — журнал действий.
- После ingest/update: обновить индекс и журнал → lint → build-site → graph → commit/push.

## Связанные заметки

- [[entities/baza-wiki|Baza Wiki]]
- [[concepts/llm-wiki|LLM Wiki]]
- [[concepts/wiki-links|Wiki Links]]
- [[SCHEMA|SCHEMA]]
