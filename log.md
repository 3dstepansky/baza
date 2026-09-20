# Wiki Log

> Хронологический журнал всех действий с базой. Append-only.
> Формат: `## [YYYY-MM-DD] действие | тема`
> Действия: ingest, update, query, lint, create, archive, delete
> Ротация: >500 записей → log-YYYY.md

## [2026-09-19] ingest | Полный архив стихов Telegram-канала Stepansky music
- Выгружены все 30 доступных сообщений канала `@Stepansky_music`; обнаружено 14 непустых текстовых публикаций.
- Сохранён immutable snapshot `raw/articles/stepansky-music-telegram-lyrics-2026-09-19.md` с датами, ID и ссылками на оригиналы.
- Созданы 14 отдельных страниц произведений в `queries/stepansky-music/`.
- Созданы каталог `queries/stepansky-music-lyrics.md` и сущность `entities/stepansky-music.md`.
- Обновлены корневой каталог и таксономия тегов (`poetry`, `lyrics`).

## [2026-09-18] ingest | Fish Audio для прямого общения агента в Яндекс.Телемосте
- Сохранён immutable research snapshot `raw/articles/fish-audio-github-research-for-telemost-2026-09-18.md` с официальными GitHub-репозиториями, API, лицензиями и ограничениями.
- Создана концепция `concepts/fish-audio-for-telemost-realtime-agent.md`.
- Рекомендован buildable MVP: Chromium + virtual audio devices + streaming STT/Hermes/Fish WebSocket TTS; Fish Agents (`fish-agent-sdk-web`, LiveKit WebRTC, custom LLM) — параллельный gated spike.
- Зафиксированы блокеры: private beta Fish Agents, отсутствие готового моста в Телемост, 24 GB VRAM и отдельная коммерческая лицензия для self-hosted Fish Speech.
- Обновлён корневой каталог.
- После параллельной проверки уточнён приоритет: buildable MVP — Chromium + virtual audio devices + streaming STT/Hermes/Fish WebSocket TTS; Fish Agents оставлен gated spike до получения private-beta доступа.
- Добавлены Node/TypeScript SDK, Pipecat integration, ограничение browser WebSocket headers, Telemost control-plane API и reference meeting-bot проекты.

## [2026-09-16] create | Интерактивный голосовой ассистент и триггеры автовыхода для Meeting Recorder
- Создана концепция `concepts/meeting-interactive-voice-agent-and-leave-triggers.md`.
- Зафиксирована архитектура Full-Duplex аудиопотока в звонке (WebRTC capture → Streaming STT → Brain/LLM RAG → Low-Latency Uniproxy TTS → Virtual Mic playback).
- Спроектирован протокол Graceful Teardown по голосовой кодовой фразе («Светочка, покинь встречу» с голосовым подтверждением и автоматической финализацией артефактов).
- Обновлены сущность `entities/telemost-recorder.md` и корневой каталог `index.md`.

## [2026-09-12] ingest | Расширенная диаграмма выгорания, недельный «Статус» и SDD-конвейер «Гелиоса»
- Сохранён immutable raw-источник `raw/transcripts/telegram-helios-extended-burndown-and-weekly-status-2026-09-12.md`.
- Создана концепция `concepts/helios-extended-burndown-weekly-status-and-sdd-delivery.md`.
- Зафиксированы недельный спринт, публичный внутренний документ «Статус», отчётный субагент, разделение исходного и добавленного scope, SDD-конвейер и два режима пользовательского тестирования.
- Добавлена аналитическая рамка burndown + burnup + cumulative flow и прогноз P50/P85 с отдельным учётом человеческих блокировок.
- Обновлён корневой каталог.

## [2026-09-10] ingest | «Партия одного вечера» и методология кифу трансформации
- Сохранён raw-источник `raw/articles/partiya-odnogo-vechera-2026-09-10.md`.
- Создана концепция `concepts/company-game-kifu-and-exploration-map.md`.
- Зафиксированы: атом-задача и CI-тест атомарности, карта разведанности L1–L5, тест воспроизводимости нарезки, четыре судьбы атома, агент как ход, эффект по потоку и кифу компании.
- Добавлены практические направления: APQC-нумерация, междоменные SLA, governance порта Actions, калибровка эталонов, L4 falsification test на CRM event log.
- Уникальность связки «штатка → разведка → слоты → эффект» сохранена как проверяемая гипотеза, а не установленный рыночный факт.
- Обновлены обратные ссылки и каталог.

## [2026-09-10] ingest | Everything as Code и Business as Code для «Гелиоса»
- Добавлен immutable raw-источник `raw/articles/everything-as-code-lecture-2026-09-10.md` по лекции Павла.
- Создана концептуальная страница `concepts/everything-as-code-for-helios.md`.
- Зафиксированы пять свойств `as Code`: декларативность, версионность, ревью, автопроверка и сверка.
- Добавлены двусторонний организационный drift, связь со шкалой наивности, границы метафоры и операционная формула «Гелиоса».
- Обновлены обратные ссылки в страницах «Гелиоса», C4 и слотовой архитектуры; обновлён каталог.

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

## [2026-08-17] ingest | LusherTale / ПсихоСказка — проектный контекст
- Создан raw source: raw/articles/lushertale-project-context-2026-08-17.md
- Созданы wiki-страницы: entities/lushertale.md, entities/nastya-wkrmst.md
- Зафиксированы: Настя `@Wkrmst` как лидер проекта, YouGile project id, NotebookLM notebook/artifact, Docker/GitHub контекст
- Обновлены index.md, concepts/mcp.md, entities/omniroute.md, SCHEMA.md
## [2026-08-18] ingest | Личный разговор с Лисным 18 августа
- Сохранён raw transcript с frontmatter/sha256: raw/transcripts/2026-08-18-lichnyy-razgovor-s-lisnym.md
- Создана обработанная wiki-страница: queries/razgovor-s-lisnym-2026-08-18.md
- Объединено с предыдущей линией 13 августа: обновлена queries/lichnoe-soveshchanie-2026-08-13.md
- Зафиксированы: стратегия «полсотни маленьких агентов», карьерная «звёздочка», роли Лисного/Олега и многоагентная разработка как инструмент Павла
- Обновлён index.md

## [2026-08-20] ingest | Лисный 19 августа — B2B-лидоген и воронка вебинара
- Сохранён raw transcript с frontmatter/sha256: raw/transcripts/2026-08-19-lisny-original.md
- Создана обработанная wiki-страница: queries/razgovor-s-lisnym-2026-08-19.md
- Зафиксирована гипотеза AI-research/квалификации для дорогих B2B-программ и безопасная opt-in альтернатива рискованным идеям о сборе данных/добавлении в чаты.
- Обновлён index.md.

## [2026-08-20] ingest | Telemost raw transcript — Telemost 2026-08-20T12-33-38-886Z
- Saved raw source: raw/transcripts/telemost-2026-08-20-12-34-23-telemost-2026-08-20t12-33-38-886z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-08-20-12-34-23-telemost-2026-08-20t12-33-38-886z-summary.md

## [2026-08-20] ingest | Telemost raw transcript — Telemost 2026-08-20T12-33-59-538Z
- Saved raw source: raw/transcripts/telemost-2026-08-20-12-56-40-telemost-2026-08-20t12-33-59-538z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-08-20-12-56-40-telemost-2026-08-20t12-33-59-538z-summary.md

## [2026-08-20] ingest | CineGI / AI-чат — интеграция автономных агентов
- Из Telemost-транскрипта создана обработанная страница: queries/cinegi-ai-chat-agent-integration-2026-08-20.md
- Обновлена entities/academic-difference-assistant.md: API-агент, богатая форма и варианты iframe/нативного виджета.
- Обновлён index.md: новая страница видна в «Быстром входе» и Queries.

## [2026-08-23] ingest | Telemost raw transcript — Telemost 2026-08-23T16-59-51-430Z
- Saved raw source: raw/transcripts/telemost-2026-08-23-20-05-59-telemost-2026-08-23t16-59-51-430z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-08-23-20-05-59-telemost-2026-08-23t16-59-51-430z-summary.md

## [2026-08-25] ingest | Идея мультиагентной системы code review для «Синергии»
- Сохранено исходное Telegram-сообщение: raw/transcripts/telegram-multi-agent-code-review-idea-2026-08-25.md
- Создана концепция: concepts/multi-agent-code-review-synergy.md
- Добавлены обратные связи из методологии многоагентной разработки и страницы ролей агентов.
- Обновлён index.md.

## [2026-08-25] ingest | Лисный — приоритеты задач и автономный AI-отдел
- UTF-16BE документ преобразован в UTF-8 и сохранён как immutable raw: raw/transcripts/lisny-prioritety-zadach-original-2026-08-25.md
- Создана структурированная заметка: queries/lisny-prioritety-zadach-2026-08-25.md
- Зафиксированы: двухнедельный коммерческий MVP, статусы приёмной комиссии и академразницы, документный бот, отложенный агент Яндекс Директа и амбиция автономного AI-отдела.
- Обновлены Academic Difference Assistant, методология многоагентной разработки, предыдущая встреча с Лисным и index.md.

## [2026-08-25] ingest | Telemost raw transcript — Telemost 2026-08-25T13-31-22-522Z
- Saved raw source: raw/transcripts/telemost-2026-08-25-14-00-33-telemost-2026-08-25t13-31-22-522z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-08-25-14-00-33-telemost-2026-08-25t13-31-22-522z-summary.md

## [2026-08-25] create | Ассистент коммерческого подразделения
- Из общей заметки о встрече с Лисным выделена профильная страница проекта: entities/commercial-department-assistant.md.
- Зафиксированы двухнедельный MVP, минимальный контур, вопросы для сбора требований и критерии готовности.
- Добавлены обратные ссылки из встречи, страницы «Продажи и Маркетинг» и index.md.

## [2026-09-03] ingest | Telemost raw transcript — Telemost 2026-09-03T10-54-09-475Z
- Saved raw source: raw/transcripts/telemost-2026-09-03-10-55-29-telemost-2026-09-03t10-54-09-475z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-09-03-10-55-29-telemost-2026-09-03t10-54-09-475z-summary.md

## [2026-09-03] ingest | Telemost raw transcript — Telemost 2026-09-03T10-55-15-076Z
- Saved raw source: raw/transcripts/telemost-2026-09-03-11-29-35-telemost-2026-09-03t10-55-15-076z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-09-03-11-29-35-telemost-2026-09-03t10-55-15-076z-summary.md

## [2026-09-07] ingest | Жизненный цикл агентов, Intake-брифинг и Гермес-пусконаладчик
- Сохранён транскрипт мыслеформы: raw/transcripts/telegram-helios-briefing-agent-forge-and-ephemeral-hermes-2026-09-07.md
- Создан концепт: concepts/helios-intake-agent-forge-and-commissioning-lifecycle.md
- Обновлена сущность: entities/hermes-agent.md и entities/helios-agent-environment.md
- Перелинковано с concepts/helios-management-dashboard-and-agent-marketplace.md и concepts/helios-slot-in-architecture-and-naivety-scale.md
- Обновлены index.md, log.md, граф и статический сайт

## [2026-09-07] ingest | Гелиос как Executive Dashboard и витрина внедрения агентов
- Сохранён транскрипт мыслеформы: raw/transcripts/telegram-helios-executive-dashboard-and-agent-showcase-2026-09-07.md
- Создан концепт: concepts/helios-management-dashboard-and-agent-marketplace.md
- Обновлена сущность: entities/helios-agent-environment.md
- Перелинковано с concepts/slot-unit-economics-and-workforce-efficiency.md и concepts/helios-slot-in-architecture-and-naivety-scale.md
- Обновлены index.md, log.md, граф и статический сайт

## [2026-09-07] ingest | Юнит-экономика слотов, время сотрудников и расчет ROI
- Сохранён транскрипт мыслеформы: raw/transcripts/telegram-slot-unit-economics-and-labor-cost-2026-09-07.md
- Создан концепт: concepts/slot-unit-economics-and-workforce-efficiency.md
- Перелинковано с concepts/helios-slot-in-architecture-and-naivety-scale.md и concepts/human-agent-socio-ethics-and-slot-displacement.md
- Обновлены index.md, log.md, граф и статический сайт

## [2026-09-07] ingest | Этика взаимодействия человек-агент, фаза дообучения и масштаб зоны интересов
- Сохранён транскрипт мыслеформы: raw/transcripts/telegram-human-agent-ethics-slot-displacement-2026-09-07.md
- Создан концепт: concepts/human-agent-socio-ethics-and-slot-displacement.md
- Перелинковано с concepts/helios-slot-in-architecture-and-naivety-scale.md и entities/helios-agent-environment.md
- Обновлены index.md, log.md, граф и статический сайт

## [2026-09-07] ingest | Архитектурный репозиторий C4 (Ветчинкин) и агентская среда «Гелиос»
- Сохранён конспект доклада ArchDays 2022 (Кирилл Ветчинкин): raw/transcripts/archdays-2022-arch-repo-c4-vetchinkin.md
- Создана концепция: concepts/c4-model-for-business-and-agents.md (адаптация C4, DocHub и семантического зума Google Maps для бизнес-архитектуры и мультиагентных сред)
- Создана сущность: entities/helios-agent-environment.md (агентская среда «Гелиос», онтология из штатного расписания, контекстная оркестрация)
- Обновлена страница: concepts/agentic-systems.md (добавлена ссылка на «Гелиос»)
- Обновлён index.md (каталог Baza)

## [2026-09-07] ingest | Слотовая архитектура замещения операций и шкала наивности «Гелиос»
- Сохранён первоисточник мыслеформы Павла: raw/transcripts/telegram-helios-c4-enterprise-model-thoughtform-2026-09-07.md
- Создана концепция: concepts/helios-slot-in-architecture-and-naivety-scale.md (Enterprise Modeler агент, шкала наивности L1-L5, Human Slot ➔ Neuro Slot, обогащение из HH/DWH)
- Обновлены entities/helios-agent-environment.md, concepts/c4-model-for-business-and-agents.md и index.md

## [2026-09-08] update | Green Broker: двухботовая модель (Питомник + Client) и брокерские продажи
- Сохранён транскрипт ввода Павла: raw/transcripts/telegram-green-broker-two-bot-architecture-and-brokerage-2026-09-08.md
- Обновлена сущность entities/green-broker.md: зафиксировано видение Павла и Романа
- Детализированы два контура: бот «Green Broker Питомник» (склад/номенклатура/deep link) и «Green Broker Client» (переговорный AI, расчет КП, проактивный retention/дожим)
- Добавлена стратегия SaaS-enabled Marketplace (собственные оптовые продажи Green Broker по остаткам питомников)
- Обновлены index.md и связи с базой знаний


## [2026-09-14] ingest | Telemost raw transcript — Telemost 2026-09-14T08-02-09-195Z
- Saved raw source: raw/transcripts/telemost-2026-09-14-08-39-51-telemost-2026-09-14t08-02-09-195z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-09-14-08-39-51-telemost-2026-09-14t08-02-09-195z-summary.md

## [2026-09-16] ingest | Telemost raw transcript — Telemost 2026-09-16T07-30-17-116Z
- Saved raw source: raw/transcripts/telemost-2026-09-16-08-17-13-telemost-2026-09-16t07-30-17-116z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-09-16-08-17-13-telemost-2026-09-16t07-30-17-116z-summary.md

## [2026-09-16] ingest | Telemost raw transcript — Лада_2
- Saved raw source: raw/transcripts/telemost-2026-09-16-12-51-09-лада-2-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-09-16-12-51-09-лада-2-summary.md

## [2026-09-16] ingest | Telemost raw transcript — Лада
- Saved raw source: raw/transcripts/telemost-2026-09-16-12-51-12-лада-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-09-16-12-51-12-лада-summary.md

## [2026-09-18] ingest | Telemost raw transcript — Эндрю_голосовой_асист
- Saved raw source: raw/transcripts/telemost-2026-09-18-12-57-03-эндрю-голосовои-асист-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-09-18-12-57-03-эндрю-голосовои-асист-summary.md

## [2026-09-18] ingest | Telemost raw transcript — Telemost 2026-09-18T13-01-41-539Z
- Saved raw source: raw/transcripts/telemost-2026-09-18-13-54-27-telemost-2026-09-18t13-01-41-539z-transcript.md
- Saved raw source: raw/transcripts/telemost-2026-09-18-13-54-27-telemost-2026-09-18t13-01-41-539z-summary.md
