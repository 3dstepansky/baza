---title: "Telemost Recorder — запись Яндекс.Телемост 🎙️"
type: entity

tags: [project, telemost, recorder, ai, docker, webrtc, telegram]
created: 2026-07-30
updated: 2026-07-31
---


# Telemost Recorder — запись Яндекс.Телемост 🎙️

**GitHub:** https://github.com/3dstepansky/stepansky-telemost-recorder-doker
**Актуальная ветка:** `v04` (релиз v0.4, коммит `508deeb4`, 02.07.2026) — соответствует спеке `specs/002-standalone-bot-and-fixes`
**Статус:** в разработке (стабильное ядро) · License MIT

Автономный ИИ-ассистент записи встреч **Яндекс.Телемост** с нулевыми операционными затратами (ZeroPay). Бот заходит в конференцию гостем, перехватывает WebRTC-аудио, транскрибирует (Groq Whisper / AssemblyAI), генерирует саммари (Groq Llama-3.3-70B) и доставляет результат в Telegram + Яндекс.Диск (WebDAV) + S3.

> ⚠️ **Важно про версии:** README в корне репозитория описывает **устаревшую** n8n-архитектуру v1.0.0. Актуальная архитектура (v0.4, spec 002) — **автономный бот без n8n** (см. ниже).

## 🏗️ Архитектура (актуальная, v0.4)

**Архитектурное решение (июль 2026): отказ от n8n.** Вся логика управления перенесена в автономный Node.js-процесс `bot.js` внутри Docker-контейнера, хранилище — SQLite. n8n-вариант (`001-telemost-recorder-core`) официально устарел.

```
Telegram (Telegraf bot.js)
      ↓
 Docker-контейнер (telemost_${CHAT_ID}_${MEETING_ID})
      ├─ recorder.js  — Puppeteer → Яндекс.Телемост → WebRTC-аудио
      ├─ run.js       — жизненный цикл записи (spawn, сигналы, webhook-стадия)
      ├─ db.js        — SQLite: пользователи, встречи, состояния FSM
      └─ services/    — ai, ffmpeg, s3, summarize, transcribe, webdav
      ↓
 Результаты: Telegram-чат (≤50 МБ) и/или Яндекс.Диск (WebDAV) + S3
```

### Что нового в v0.4 (vs старый master)

1. **Мульти-запись и защита от дубликатов** — имена контейнеров `telemost_${CHAT_ID}_${MEETING_ID}`, параллельные сессии; повторный старт той же встречи блокируется
2. **Персональные имена ботов** — для каждого `chat_id` своё отображаемое имя (поле `bot_display_name` в БД)
3. **Умный run_stop.sh** — точечная остановка по `MEETING_ID` или групповая по `CHAT_ID`
4. **Устранение Race Condition** — выгрузка (S3/Диск) гарантированно **до** уведомления оркестратора, чтобы файл не удалился при копировании
5. **Лимит контекста LLM** — 25 000 символов на текст для суммаризатора (`services/summarize.js`)
6. **Telegram без Яндекс.Диска** — запись присылается прямо в чат (до 50 МБ ≈ 1.5 ч); текст и саммари приходят всегда

## 📁 Файловая структура (v04)

| Файл | Назначение |
|------|-----------|
| `bot.js` (15 КБ) | Автономный Telegram-бот на **Telegraf**: меню, FSM, команды `/start /record /ai`, HTML-формат сообщений |
| `recorder.js` (19 КБ) | WebRTC-интерцептор: вход, обход лобби, захват аудио, anti-zombie (`try/finally` + SIGTERM/SIGINT) |
| `run.js` (5 КБ) | Жизненный цикл записи в контейнере, spawn-процессы, стадия уведомления |
| `db.js` (3.5 КБ) | SQLite-слой: `getUser/saveUser/getRecentMeetings`, состояния FSM |
| `transcribe.js` | Транскрибация (Groq/AssemblyAI) |
| `upload_audio.js` | Выгрузка исходного аудио |
| `local_bridge.js` | Локальный мост для отладки без контейнера |
| `mock_n8n.py` | Мок оркестратора (наследие n8n-эпохи) |
| `verify_rename_and_summarize_mock.js` | Проверка переименования и саммари |
| `services/ai.js` | Groq **Whisper-large-v3**: `verbose_json`, сегменты → utterances, `speaker_count=1` (заглушка диаризации) |
| `services/ffmpeg.js` | Сегментация **без перекодирования** (`-c copy`), чанки 1200 сек, лимит 24.5 МБ |
| `services/summarize.js` | Бизнес-саммари: ключевые темы, решения, Next Steps; модель `llama-3.3-70b-versatile`, обрезка 25K символов |
| `services/webdav.js` | Яндекс.Диск: создание папок (405-игнор), Basic auth, `Yandex.Telemost.Records/[Дата]_[Тема]/` |
| `services/s3.js` | Универсальная S3-выгрузка (MinIO/Яндекс Облако/AWS), пропуск если ключи не заданы |
| `services/transcribe.js` | Транскрибация-сервис (вынесен в pipeline) |
| `run_join.sh / run_start.sh / run_stop.sh` | Скрипты запуска/остановки (совместимость с внешними вызовами) |
| `run_transcribe.sh / run_upload.sh` | Этапы обработки |
| `set_recorder_display_name.sh` | Имя бота на встрече |
| `database.sql` | Схема PostgreSQL/Supabase (историческая; актуально — SQLite в `db.js`) |
| `docker-compose.yml` | Сервис `recorder`, volume `./recordings`, env_file `.env` |
| `Dockerfile` / `Dockerfile.test` | Боевой образ и тестовый |
| `test/db.test.js` | Юнит-тесты БД (`node --test`) |
| `specs/002-standalone-bot-and-fixes/` | **Актуальная спека**: US-1…US-16 |
| `specs/003-speaker-names-and-ai-summary/` | Спека имён спикеров и AI-саммари |
| `MULTICHANNEL_HYPOTHESIS_ROADMAP.md` | Доркарта гипотезы US-16 (диаризация по WebRTC-трекам) |
| `n8n_workflow_v0.4.json` / `n8n_workflow_head.json` | Воркфлоу n8n (исторические) |
| `.agents/skills/` | Навыки для ИИ-агентов разработки |
| `.specify/` | Конфиг Specify (ИИ-спецификации): feature.json, integration.json, workflows |

## 🗄️ База данных

**Актуально (SQLite, `db.js`):** пользователи, состояния FSM, настройки (имя бота, Яндекс.Диск), история встреч.

**Историческая схема PostgreSQL (`database.sql`):**

- **`telemost_meeting_transcripts`** — id, title, file_path, chat_id, transcript, summary, speaker_count, utterance_count, utterances (JSONB с таймингами), transcribed_at, operation_id (unique — защита от дублей)
- **`telemost_user_settings`** — chat_id, state, yandex_user, yandex_webdav_password, **bot_display_name** (персональное имя бота)

## 🤖 Telegram-интерфейс (bot.js, Telegraf)

Клавиатуры: `MAIN_MENU` (🔴 Запись / 🧠 Аналитика / ⚙️ Настройки / ℹ️ Помощь), `AI_MENU` (📝 Транскрибировать / 💡 Саммари / 📂 Список встреч), `SETTINGS_MENU` (👤 Имя бота / 📦 Яндекс.Диск).

- **🔴 Запись** — состояние `wait_for_link`, ждёт ссылку `https://telemost.yandex.ru/j/...`, бот заходит под именем `bot_name`
- **🧠 Аналитика** — ручная транскрибация, саммари, список встреч (ИИ-названия)
- **⚙️ Настройки** — имя бота, подключение Яндекс.Диска прямо из Telegram
- **Fallback без Диска** — аудио в чат до 50 МБ, предупреждение в UI

## 🧪 Гипотеза US-16: нативная диаризация (MULTICHANNEL_HYPOTHESIS_ROADMAP)

Цель: Яндекс.Телемост отдаёт **отдельные WebRTC-аудиотреки по участникам** — можно писать их раздельно и строить карту диаризации без потери авторства.

- Субагент-наблюдатель: **`multichannel-hypothesis-tracker`** (фиксирует изменения, проверки, статусы)
- Текущее состояние кода: `recorder.js` сводит все треки в один mix через `MediaStreamDestination` (строки 121-143)
- Статус шагов: [x] тестовый контейнер (02.07.2026), [~] track-level запись (нужна привязка имён), [x] ранняя выгрузка исходного аудио в папку встречи, [ ] мастер-формат, [ ] diarization_map.json, [ ] сопоставление с AssemblyAI, [ ] перенос в основной pipeline
- **US-16 в спеке 002 — статус «✅ Реализовано (Dual-Output Архитектура)»**

## 📋 Статус требований (spec 002, 02.07.2026)

| ID | Требование | Статус |
|----|-----------|--------|
| US-1 | Запись WebRTC-аудио (вход в комнату) | ✅ |
| US-2 | Автозавершение и Anti-Zombie | ✅ |
| US-3 | Автономный Telegram-бот (замена n8n) | ✅ |
| US-4 | Автовыход при завершении встречи организатором | ✅ |
| US-5 | Информационный стиль Ильяхова | ✅ |
| US-6 | Транскрибация с диаризацией (AssemblyAI + Groq fallback) | ⚠️ пайплайн есть, диаризация не протестирована |
| US-7 | Выгрузка на Яндекс.Диск + S3 | ⚠️ требует проверки |
| US-8 | ИИ-саммари и рассылка в Telegram | ✅ |
| US-9 | Быстрый старт по ссылке с inline-кнопкой | ✅ |
| US-10 | Персональное имя бота | ✅ (SQLite) |
| US-11 | ИИ-переименование папок на Диске | ⚠️ частично |
| US-12 | Интеграция с Яндекс.Календарём | ❌ |
| US-13 | Просмотр архива встреч в Telegram | ⚠️ базовый список |
| US-14 | Чат-ассистент по встрече (RAG) | ❌ |
| US-15 | Живой ИИ-агент в комнате (Real-Time STT/TTS) | ❌ |
| US-16 | Нативная диаризация через WebRTC-треки | ✅ (Dual-Output) |

## 🛠️ Стабилизация (STABILIZATION_REPORT, v0.003 → v0.4)

- **Docker gateway `172.19.0.1`** — SSH из контейнера n8n наружу (исторически)
- **SSH-ключ `id_rsa_n8n`** — обход PAM/fail2ban на Oracle Ubuntu 24.04 (исторически)
- **Anti-Zombie** — `--init` флаг + `try/finally` + `browser.close()` в 100% случаев (найдено 85 зомби-процессов Chrome)
- **Base image `node:20-slim`** — фикс сборки ARM64
- **Webhook-First / Order-First** — транскрибация/выгрузка строго после готовности файла

## 🧰 Стек

Node.js v20+ · Puppeteer 24 · Telegraf 4.16 · FFmpeg · Groq SDK (Whisper-large-v3, Llama-3.3-70B) · AssemblyAI · @aws-sdk/client-s3 · SQLite · Docker · WebDAV (Яндекс.Диск) · n8n (исторически) · Specify (.specify/)

## 🎯 Roadmap v2

- 🔴 **Diarization** — разделение реплик по спикерам (гипотеза US-16)
- 🔴 **Real-Time AI Chat** — вопросы боту по контексту во время записи
- 🔴 **Archival Q&A** — чат по историческим встречам с Диска (RAG)

## 🔗 Перекрёстные ссылки

- [[index|Проекты]] — хаб
- [[index|КПН-Агент]] — схожий пайплайн: стенограммы → саммари → реестр поручений
- [[index|Расшифровки встреч]] — транскрипты совещаний холдинга
- [[concepts/free-ai-methods|Методы бесплатного доступа]] — Groq, OpenRouter, free-tier
- [[entities/omniroute|OmniRoute]] — AI-прокси (OpenRouter-подобный слой)
- [[concepts/agentic-systems|Агентные системы]] — субагент-наблюдатель мультиканальной гипотезы
- [[concepts/llm-wiki|LLM Wiki]] — доркарта ведётся субагентом, как эта база знаний
- [[entities/hermes|Hermes Agent]] — агентная разработка (.agents/skills)
- [[entities/python|Python]] — наследие mock_n8n.py, инструменты разработки
- [[concepts/mcp|MCP]] — интеграции с ботами/платформами
