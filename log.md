# Wiki Log

> Хронологический журнал всех действий с базой. Append-only.
> Формат: `## [YYYY-MM-DD] действие | тема`
> Действия: ingest, update, query, lint, create, archive, delete
> Ротация: >500 записей → переименовать в log-YYYY.md, начать новый.

## [2026-07-30] create | Wiki инициализирована
- Domain: персональная база знаний (AI/ML, dev, trading, projects, synergy)
- Структура: хабы по разделам, MCP baza, публикация _site/
- Заметки: omniroute.md, vibecoder-sources.md, AI-Freebies.md и др.

## [2026-07-30] ingest | OmniRoute исследование
- Отчёты: omniroute-free-tier-providers-report.md, omniroute-technical-documentation.md
- В базу: AI-ML/omniroute.md

## [2026-07-31] update | Обогащение вики (ликвидация заглушек)
- 15 stub-заметок заполнены контентом (Dev, Concepts, System, Trading, Projects)
- 18 сирот → 0, 131 резолвнутых ссылок
- Обновлены все хабы; commit eb86093

## [2026-07-31] update | Фикс графа
- Клик по узлу вёл на .md → 404; исправлено на .html (generate-graph.py)
- Питфолл записан в obsidian-knowledge-base

## [2026-07-31] ingest | Проект Telemost Recorder
- Изучен репозиторий stepansky-telemost-recorder-doker (ветка v04!)
- Projects/Telemost-Recorder.md: v0.4, автономный бот (без n8n), US-1..16, мультиканал
- Commit d041dfe

## [2026-07-31] update | Стандарт: индекс, хабы, окружение
- WIKI_PATH + OBSIDIAN_VAULT_PATH установлены в ~/.hermes/.env → /home/ubuntu/baza
- 9 вложенных index.md переименованы в <Раздел>.md (только корневой index.md остался) → [[index]] кликабелен
- Корневой index.md перестроен по шаблону llm-wiki: каталог всех 51 страниц с one-line summary
- 32 файла обновлены (ссылки [[Раздел/index|...]] → [[Раздел/Раздел|...]])
- SCHEMA.md: правило «только один index.md», обновлена структура
- Итог: 235 ссылок, 1 index.md, 0 сирот/битых

## [2026-07-31] lint | Полная пересборка по методологии llm-wiki
- 13-пунктовый lint: 54 проблемы → 0
- Добавлены перекрёстные ссылки в 24 заметки (минимум 2 исходящие)
- Таксономия тегов расширена в SCHEMA.md (53+ тегов, 3 новых категории)
- confidence: medium на быстро меняющиеся темы (omniroute, vibecoder-sources, free-ai-methods)
- Synergy/Org-Structure.md перенесён в raw/org-structure.md (Layer 1, immutable)
- Frontmatter добавлен во все заметки (0 без frontmatter)
- Итог: 0 сирот, 0 битых ссылок, 205 ссылок, 51 заметка

## [2026-07-31] create | Внедрение методологии llm-wiki (скилл v2.1.0)
- Установлен официальный скилл research/llm-wiki (507 строк)
- Созданы SCHEMA.md (конвенции, таксономия тегов, пороги) и log.md
- obsidian-knowledge-base помечен как специфика; llm-wiki — главная методология
