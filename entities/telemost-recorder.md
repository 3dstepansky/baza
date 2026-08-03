---
title: Telemost Recorder — запись Яндекс.Телемост
created: 2026-07-30
updated: 2026-08-03
type: entity
tags: [entity, project, bot, automation, meeting, transcript, node, docker, telegram, whisper]
sources: [raw/articles/telemost-recorder-repository-v04-2026-08-03.md]
confidence: high
---

# Telemost Recorder — запись Яндекс.Телемост 🎙️

**GitHub:** https://github.com/3dstepansky/stepansky-telemost-recorder-doker  
**Актуальная ветка:** `v04` — коммит `508deeb` от 2026-07-03 (`feat: direct telegram delivery and ai summary fix`).  
**Важно про версии:** `master` и `003v` старее (`b563afd`, 2026-05-31) и README частично продолжает описывать n8n-оркестрацию. Актуальный код и спецификация `002-standalone-bot-and-fixes` фиксируют переход к автономному Node.js/Telegram-боту без n8n как основного оркестратора. ^[raw/articles/telemost-recorder-repository-v04-2026-08-03.md]

## Суть проекта

**Telemost Recorder** — zero-cost бот для записи встреч в **Яндекс.Телемосте**. Он заходит на встречу гостем, перехватывает WebRTC-аудио через Puppeteer/Chromium, сохраняет `.webm`, транскрибирует встречу через AssemblyAI или Groq Whisper, генерирует саммари через Groq Llama 3.3 70B, а затем отдаёт результаты в Telegram и/или Яндекс.Диск через WebDAV. ^[raw/articles/telemost-recorder-repository-v04-2026-08-03.md]

Проект важен для базы как живой пример [[concepts/agentic-systems|агентной автоматизации]] вокруг встреч: браузерный агент действует в видеоконференции, извлекает аудио, строит пайплайн STT → summary → delivery и закладывает будущий RAG/архив встреч.

## Архитектура v04

```text
Telegram bot.js / Telegraf
  ↓
run.js — жизненный цикл сессии
  ↓
recorder.js — Puppeteer + WebRTC monkey-patch + MediaRecorder
  ↓
recordings/<timestamp>/
  ├── meeting_audio.webm
  ├── tracks/<trackId>.webm
  └── meta/track_events.ndjson, tracks_summary.json
  ↓
transcribe.js
  ├── AssemblyAI speaker_labels=true
  └── Groq Whisper fallback через FFmpeg chunks
  ↓
summary.txt / transcript.txt / Telegram / Yandex Disk / S3
```

Ключевой архитектурный сдвиг: в старой версии n8n был внешним orchestrator-слоем, а в v04 основной пользовательский контур перенесён в `bot.js` + SQLite. n8n-файлы (`n8n_workflow_v0.4.json`, `n8n_workflow_head.json`) остаются в репозитории как исторические/совместимые артефакты. ^[raw/articles/telemost-recorder-repository-v04-2026-08-03.md]

## Основные компоненты

| Компонент | Назначение |
|---|---|
| `bot.js` | Telegram-бот на Telegraf: меню, FSM, настройки имени бота и Яндекс.Диска, старт/стоп записи |
| `run.js` | Запускает `recorder.js`, после закрытия записи делает раннюю выгрузку аудио и запускает транскрибацию |
| `recorder.js` | Headless Chromium/Puppeteer, вход в Телемост, WebRTC monkey-patch, запись mix + per-track файлов |
| `transcribe.js` | AssemblyAI → Groq fallback, speaker mapping по `track_events.ndjson`, выгрузка transcript/summary, отправка в Telegram |
| `db.js` | SQLite: `users`, `meetings`, state FSM, имя бота, WebDAV-учётки |
| `services/webdav.js` | Яндекс.Диск через WebDAV: MKCOL, PUT, MOVE, проверка авторизации |
| `services/summarize.js` | Саммари и метаданные папки через Groq `llama-3.3-70b-versatile` |
| `services/transcribe.js` | AssemblyAI `speaker_labels=true`, Groq Whisper `verbose_json` fallback |
| `services/ffmpeg.js` | Конвертация/сегментация аудио для STT |
| `.specify/` и `.github/prompts/speckit.*` | Spec Kit / Specify контур для spec-driven разработки |

## UX Telegram-бота

Бот имеет три главных пользовательских раздела:

- **🔴 Запись встреч** — ждёт ссылку вида `https://telemost.yandex.ru/j/...`, заходит в комнату под пользовательским именем, даёт inline-кнопку «Остановить».
- **🧠 Аналитика и ИИ** — список встреч, транскрипция, саммари. В текущем `bot.js` кнопки «Сделать саммари» и «Транскрибировать» ещё выглядят как заглушки, но автоматическая обработка после записи реализована в `transcribe.js`.
- **⚙️ Настройки** — имя бота и подключение Яндекс.Диска через 16-значный WebDAV app password. Если Диск не подключен, бот пытается присылать файлы прямо в Telegram до лимита 50 МБ.

## База данных

Актуальная SQLite-схема в `db.js`:

```sql
users(chat_id primary key, bot_name, yandex_user, yandex_pass, state)
meetings(id, chat_id, meeting_id, title, file_path, transcribed_at, speaker_count, utterance_count)
```

Историческая `database.sql` описывает PostgreSQL/Supabase-таблицы `telemost_meeting_transcripts` и `telemost_user_settings`, но для v04 рабочий runtime — SQLite внутри контейнера. ^[raw/articles/telemost-recorder-repository-v04-2026-08-03.md]

## Статус требований spec 002

Реализовано:

- запись WebRTC-аудио и вход в комнату;
- anti-zombie завершение Chromium через `try/finally`, `dumb-init`, SIGINT/SIGTERM;
- автономный Telegram-бот вместо n8n;
- автовыход при завершении встречи/idle/max duration;
- инфостиль сообщений;
- быстрый старт по ссылке;
- персональное имя бота;
- ИИ-саммари и отправка результата в Telegram;
- dual-output WebRTC: общий mix + отдельные per-track `.webm` + события активности.

Частично/требует проверки:

- AssemblyAI-диаризация и сопоставление с локальной картой треков;
- выгрузка на Яндекс.Диск/S3 в реальном окружении;
- ИИ-переименование папок WebDAV `MOVE`;
- архив встреч в Telegram пока базовый.

Не начато / roadmap:

- Яндекс.Календарь;
- RAG-чат по встрече;
- живой STT/TTS-агент внутри комнаты.

## US-16: нативная диаризация через WebRTC-треки

Самая важная исследовательская линия проекта — гипотеза, что Яндекс.Телемост отдаёт отдельные WebRTC-аудиотреки по участникам. В v04 `recorder.js` уже реализует dual-output:

1. `meeting_audio.webm` — общий микс для STT.
2. `tracks/<trackId>.webm` — отдельная запись каждого входящего аудиотрека.
3. `meta/track_events.ndjson` — события `track-added` и `speech-segment` с `trackId`, временем и амплитудой.
4. `tracks_summary.json` — сводка по трекам.

Проверка track-probe на реальной встрече 2026-07-02 подтвердила техническую возможность раздельной записи: получены два отдельных `.webm` трека и события активности. Ограничение: `speakerName` пока пишется как `unknown`, нужно улучшить DOM-маппинг имени участника. ^[raw/articles/telemost-recorder-repository-v04-2026-08-03.md]

## Проверка и качество

Я проверила тесты в актуальной ветке `v04`:

```text
npm install
npm test

# tests 3
# suites 1
# pass 3
# fail 0
```

Первый запуск `npm test` падал из-за отсутствующих зависимостей (`sqlite3` не установлен). После `npm install` тесты `test/db.test.js` прошли: создание дефолтного пользователя, сохранение и обновление пользователя. `npm install` также показал `npm audit`: 16 vulnerabilities, включая 1 critical — это отдельный quality-gate перед production. ^[raw/articles/telemost-recorder-repository-v04-2026-08-03.md]

## Риски и технический долг

- **README drift:** корневой README смешивает старую n8n-архитектуру и v0.4; для ориентации читать ветку `v04`, `specs/002`, `.specify/memory/constitution.md` и код.
- **Секреты:** `yandex_pass` хранится в SQLite; для production нужен отдельный security review и шифрование/секрет-хранилище.
- **Speaker names:** WebRTC track-level запись подтверждена, но имена участников пока нестабильны (`unknown`).
- **Telegram file limit:** без Яндекс.Диска аудио >50 МБ не отправится, хотя текст/саммари должны приходить.
- **Vulnerabilities:** после `npm install` зафиксированы 16 audit issues.
- **Puppeteer fragility:** вход в Телемост зависит от DOM/селекторов Яндекса.
- **RAG privacy:** будущий архивный поиск должен быть жёстко изолирован по `chat_id`, как прописано в конституции.

## Roadmap

1. Починить `speakerName`: сопоставление WebRTC trackId с DOM-именем участника.
2. Зафиксировать мастер-формат диаризации: `mix + per-track` или полноценный `diarization_map.json`.
3. Проверить WebDAV/S3 upload и MOVE-переименование на реальном Яндекс.Диске.
4. Довести ручные кнопки «Транскрибировать»/«Сделать саммари» в Telegram UI.
5. Закрыть `npm audit` / обновить уязвимые зависимости.
6. Реализовать архивный RAG-Q&A по встречам с изоляцией по `chat_id`.
7. Исследовать real-time STT/TTS агента в комнате с latency <1.5 сек.

## Связанные заметки

- [[concepts/agentic-systems|Агентные системы]]
- [[concepts/spec-driven-agent-development|Spec-driven агентная разработка]]
- [[concepts/multi-agent-development-methodology|Методология многоагентной разработки automation-проектов]]
- [[concepts/free-ai-methods|Бесплатное использование нейросетей]]
- [[entities/hermes|Hermes Agent — инфраструктура]]
- [[entities/green-broker|Green Broker]]
- [[concepts/mcp|MCP — Model Context Protocol]]
