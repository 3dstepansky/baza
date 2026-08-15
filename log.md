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

## [2026-08-02] ingest | Green Broker — реальный проект Telegram-бота для продажи растений
- Сохранены raw-источники: raw/articles/green-broker-constitution-2026-08-02.md, raw/articles/green-broker-spec-2026-08-02.md, raw/articles/green-broker-plan-2026-08-02.md
- Создана wiki-страница entities/green-broker.md
- Обновлены concepts/spec-driven-agent-development.md, concepts/multi-agent-development-methodology.md, index.md
- Зафиксировано: Green Broker — собственный проект Павла, оформленный через Constitution → Spec → Plan; MVP фокусируется на B2B-заявках ландшафтников, виртуальной корзине и PDF КП

## [2026-08-02] ingest | Green Broker — коммерческие предложения PDF
- Извлечён текст из PDF и сохранены raw-страницы: raw/articles/green-broker-kp-pitomniki-2026-08-02.md, raw/articles/green-broker-kp-telegram-bot-2026-08-02.md
- Оригинальные PDF сохранены как raw/assets/green-broker/KP-pitomniki.pdf и raw/assets/green-broker/KP-telegram-bot.pdf
- Обновлена entities/green-broker.md: добавлен go-to-market слой, pricing, модель подписки питомников и этапы из КП
- Обновлён index.md

## [2026-08-03] update | Telemost Recorder — исследование актуальной ветки v04
- Исследован репозиторий https://github.com/3dstepansky/stepansky-telemost-recorder-doker: ветки master/003v/test/v04, актуальная ветка v04 (`508deeb`, 2026-07-03)
- Создан raw snapshot: raw/articles/telemost-recorder-repository-v04-2026-08-03.md
- Полностью обновлена entities/telemost-recorder.md: архитектура v04, компоненты, UX, SQLite, US-16, roadmap, риски
- Проверка: `npm install && npm test` в `/tmp/telemost-repo` → 3 теста прошли; npm audit сообщает 16 vulnerabilities
- Обновлён index.md
## [2026-08-03] ingest+lint | Academic Difference Assistant и LLM Wiki lint
- Добавлены raw-источники: raw/transcripts/academic-difference-assistant-meeting-2026-08-03-transcript.md, raw/transcripts/academic-difference-assistant-meeting-2026-08-03-summary.md
- Создана wiki-страница entities/academic-difference-assistant.md
- Расширена SCHEMA.md tag taxonomy для полного llm-wiki lint
- Обновлён index.md и queries/README.md
## [2026-08-04] update | Telegram source @cryptoperchikk
- Подписка через Telegram MCP: @cryptoperchikk / cryptoperchik, chat_id=-1003135147918
- Обновлена entities/vibecoder-sources.md: добавлен канал как источник AI/API/вайбкодинг/low-price моделей
- Проверены последние сообщения через MCP: Agent Router, Opus 5, GPT 5.6 sol, MCP tunnel для ChatGPT
## [2026-08-04] update | Telegram source @startup_14day
- Подписка через Telegram MCP: @startup_14day / «Автоматизируй и властвуй», chat_id=-1002382736969
- Обновлена entities/vibecoder-sources.md: добавлен канал как источник по AI automation/no-code/business workflows
- Проверены последние сообщения через MCP: telegram-mcp, Kimi K3/BIM, Qwen 3.6, AI code-review routing
## [2026-08-04] update | Telegram source @myttsinfo
- Подписка через Telegram MCP: @myttsinfo / MyTTS, chat_id=-1001548578320
- Обновлена entities/vibecoder-sources.md: добавлен TTS/voice источник для мониторинга SAPI/Silero/Google TTS и русских голосов
- Проверены последние сообщения через MCP: NaturalVoiceSAPIAdapter, SAPI 5 Svetlana, Balabolka, сравнение ru_roman/ru_alexandr/Silero
## [2026-08-04] update | Telegram source @aikirichenko
- Подписка через Telegram MCP: @aikirichenko / AI Kirichenko, chat_id=-1002300353962
- Обновлена entities/vibecoder-sources.md: добавлен канал как источник по AI education, Claude Code/n8n automation, GitHub-подборкам
- Проверены последние сообщения через MCP: system-design-primer, last30days-skill, coding-interview-university, awesome-python, Opus 5/Claude Code
## [2026-08-04] update | Telegram invite source ИИмерсивный
- Вступление через Telegram MCP по invite link `https://t.me/+eH-qNIDmud8zNDZi`, chat_id=-1003695481859
- Обновлена entities/vibecoder-sources.md: добавлен источник по AI startup diary, Claude/Fable/Sol workflows и agent skills
- Проверены последние сообщения через MCP: /grill-me, Anki word clipper, Gemini 2.5 Flash, Fable/Sol comparisons

## [2026-08-15] update | Telegram vibe-coding sources subscription
- Подписка через Telegram MCP: @vibecoding_tg / «Вайб-кодинг», chat_id=-1001555418015, status=joined
- Подписка через Telegram MCP: @vibe_coders / Vibe coders (n8n, ai, python), chat_id=-1002630631887, status=joined
- Запрос на вступление через Telegram MCP: @vibecoding_ua / «Вайб-Кодинг», chat_id=-1002736221406, status=requested (`InviteRequestSent`)
- Запрос на вступление через Telegram MCP: @bot_devs_novice / Vibecoding Haven Chat (BotfatherDEV), chat_id=-1001415356906, status=requested (`InviteRequestSent`)
- Обновлена entities/vibecoder-sources.md: статусы подписки/запросов и описания источников

## [2026-08-04] update | Telegram source @aiforbusinesswolf
- Подписка через Telegram MCP: @aiforbusinesswolf / «AI для бизнеса | Эндрю Вольф», chat_id=-1002942426023
- Обновлена entities/vibecoder-sources.md: добавлен источник по AI transformation/business automation
- Проверены последние сообщения через MCP: Plaud, Genspark, Perplexity, Julius для предпринимателей
## [2026-08-09] ingest | Construction Maps MCP Server — кадастр и полигоны
- Создан raw snapshot: raw/articles/construction-maps-mcp-repository-2026-08-09.md
- Создана wiki-страница: entities/construction-maps-mcp.md
- Зафиксировано: сервер отвечает за кадастровые границы, полигоны/геометрию, Rosreestr/НСПД + Yandex Maps; выбран под будущую автоматизацию
- Обновлены index.md и concepts/mcp.md
## [2026-08-09] update+lint | Construction Maps MCP — навигация и связь с Green Broker
- Главная index.md дополнена быстрым входом и секцией Automation / MCP, чтобы страницу было видно с главной
- construction-maps-mcp.md связан с Green Broker и рабочим контекстом Романа/садового проекта
- green-broker.md получил обратную ссылку на Construction Maps MCP как потенциальный картографический слой
- После правок запущен lint vault
## [2026-08-10] ingest | Telemost 2026-08-10 — Student Appeals Agent
- Сохранено ИИ-саммари встречи: raw/transcripts/telemost-2026-08-10-student-appeals-agent-summary.md
- Создана wiki-страница: entities/student-appeals-agent.md
- Зафиксировано: агент контроля обращений студентов должен подключаться к почтовым ящикам, контролировать сроки обработки и отправлять уведомления/отчеты через Telegram
- Обновлён index.md

## [2026-08-10] ingest | Карта Тройка — GitHub research
- Сохранён raw snapshot: raw/articles/troika-card-github-research-2026-08-10.md
- Созданы wiki-страницы: entities/troika-card.md, concepts/nfc-rfid-transport-cards.md, concepts/security.md
- Зафиксированы репозитории: TroikaDumper, Metrodroid, Farebot, SuperTroika Wiki, Proxmark3, Metroflip и связанные проекты
- Обновлены SCHEMA.md и index.md
## [2026-08-11] create | Российские grocery-приложения и MCP-серверы — план исследования
- Создана query-страница: queries/russian-grocery-mcp-research-plan.md
- Зафиксированы целевые приложения: Самокат, Пятёрочка, Перекрёсток, Лента, Магнит, Красное и Белое, Евроспар
- План: искать готовые MCP, не-MCP API-клиенты, web/mobile endpoints и оценивать возможность безопасного MCP-адаптера без автооплаты
- Обновлены index.md, SCHEMA.md, concepts/mcp.md, entities/hermes-marketplace-tools.md

## [2026-08-13] ingest | Telemost raw transcript — Telemost 2026-08-13T14-53-25-728Z
- Saved raw source: raw/transcripts/telemost-2026-08-13-14-54-43-telemost-2026-08-13t14-53-25-728z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-08-13-14-54-43-telemost-2026-08-13t14-53-25-728z-summary.md

## [2026-08-13] ingest | Telemost raw transcript — Telemost 2026-08-13T19-49-46-883Z
- Saved raw source: raw/transcripts/telemost-2026-08-13-19-55-24-telemost-2026-08-13t19-49-46-883z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-08-13-19-55-24-telemost-2026-08-13t19-49-46-883z-summary.md

## [2026-08-13] ingest | Telemost raw transcript — Telemost 2026-08-13T19-57-49-099Z
- Saved raw source: raw/transcripts/telemost-2026-08-13-21-07-21-telemost-2026-08-13t19-57-49-099z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-08-13-21-07-21-telemost-2026-08-13t19-57-49-099z-summary.md

## [2026-08-14] create | Разговор с Анной — личный компас и три слова
- Создана обработанная wiki-страница: queries/razgovor-s-annoy-2026-08-13.md
- Связана с raw-транскриптом Telemost 2026-08-13T19-57-49Z
- Зафиксирована рабочая триада разговора: органичность — влияние — наслаждение
- Обновлён index.md: Queries и Raw

## [2026-08-15] ingest | Личное совещание 13 августа
- Сохранён raw transcript: raw/transcripts/2026-08-13-lichnoe-soveshchanie-original.md
- Создана обработанная wiki-страница: queries/lichnoe-soveshchanie-2026-08-13.md
- Обновлены связи: entities/academic-difference-assistant.md и entities/student-appeals-agent.md
- Обновлён index.md
