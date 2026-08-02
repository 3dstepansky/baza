# Wiki Log

> Хронологический журнал всех действий с базой. Append-only.
> Формат: `## [YYYY-MM-DD] действие | тема`
> Действия: ingest, update, query, lint, create, archive, delete
> Ротация: >500 записей → log-YYYY.md

## [2026-07-31] create | Wiki пересобрана с нуля по стандарту llm-wiki v2.1.0
- Структура: entities/ concepts/ comparisons/ queries/ raw/{articles,papers,transcripts,assets} _archive/
- 46 страниц реклассифицированы по типам (entity/concept), хабы архивированы
- raw/: отчёты OmniRoute + 5 расшифровок встреч (sha256, immutable)
- SCHEMA.md: домен, конвенции, frontmatter, таксономия 30 тегов, thresholds
- index.md: каталог всех страниц (секции: Entities/Concepts/Comparisons/Queries/Raw)
- comparisons/free-tier-providers.md создана
- WIKI_PATH=/home/ubuntu/baza установлен
- 35 файлов перелинкованы под новую структуру

## [2026-08-02] create | Каркас исследования многоагентной разработки automation-проектов
- Созданы raw-источники: 11 файлов (GitHub, Web/arXiv, Telegram MCP-срез)
- Созданы wiki-страницы: 5 файлов
- Обновлены SCHEMA.md (таксономия), index.md (каталог)
- Тема стартует как долгий исследовательский проект: raw → wiki → synthesis → NotebookLM podcast

## [2026-08-02] update | Spec Kit как коммуникационный каркас
- Зафиксировано: Павел знаком с GitHub Spec Kit и конструкцией project → spec → plan → tasks → implement
- Обновлены concepts/spec-driven-agent-development.md и concepts/multi-agent-development-methodology.md
- Spec Kit назначен базовым языком коммуникации для многоагентной методологии automation-проектов

## [2026-08-02] ingest | Apply Pilot как живой кейс multi-agent/spec-driven разработки
- Создан raw/transcripts/apply-pilot-context-2026-08-02.md с контекстом от Павла
- Создана entities/apply-pilot.md
- Обновлены concepts/multi-agent-development-methodology.md, SCHEMA.md, index.md
- Зафиксировано ограничение: Павел участвует ресурсами, но не является инициатором/методологическим владельцем/продуктовым владельцем проекта
