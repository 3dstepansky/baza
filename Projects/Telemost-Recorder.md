---
tags: [project, telemost, recorder, ai, docker, n8n]
---

# Telemost Recorder — запись Яндекс.Телемост 🎙️

**GitHub:** https://github.com/3dstepansky/stepansky-telemost-recorder-doker
**Версия:** v1.0.0 (ядро v0.003, стабилизировано)
**Статус:** stable · License MIT

Автономный ИИ-ассистент для записи встреч **Яндекс.Телемост** с **нулевыми операционными затратами** (ZeroPay). Бот заходит в конференцию гостем, перехватывает WebRTC-аудио, транскрибирует через Groq Whisper, генерирует саммари через OpenRouter и выгружает всё на Яндекс.Диск. Управление — через Telegram.

## Ключевые особенности

1. **Headless WebRTC Injection** — запись аудио перехватом потоков из `RTCPeerConnection` в изолированном Puppeteer-контейнере
2. **Whisper-Friendly Chunking** — нарезка FFmpeg на чанки по 20 минут (обход лимита Groq Whisper 25 MB)
3. **Storage Self-Cleaning** — гарантированное удаление локальных файлов после выгрузки
4. **Яндекс.Диск (WebDAV)** — автосохранение в `Yandex.Telemost.Records/[Дата]_[Тема_от_ИИ]/`
5. **Multi-User Isolation** — отдельный Docker-контейнер `telemost_<chat_id>` на пользователя
6. **n8n Orchestration & FSM** — воркфлоу n8n управляет Telegram-интерфейсом, PostgreSQL и процессами

## Архитектура

Два слоя: **исполнительный** (Docker-воркер на хосте) + **оркестрирующий** (n8n).

```
Telegram → n8n Orchestrator → SSH Exec → Docker (telemost_<chat_id>)
                                        │  Puppeteer → Телемост (WebRTC)
                                        │  FFmpeg: VAD + сегментация
                                        ↓
                              Webhook ← контейнер (сигнал «аудио готово»)
                                        ↓
           n8n → Groq Whisper (транскрибация) → OpenRouter (саммари)
                                        ↓
           Telegram отчёт + Яндекс.Диск (WebDAV) + PostgreSQL
```

## Файловая структура

| Файл | Назначение |
|------|-----------|
| `recorder.js` | WebRTC-интерцептор: вход, обход лобби, захват аудио, anti-zombie (try/finally + SIGTERM/SIGINT) |
| `run.js` | Оркестрация внутри контейнера, webhook-first уведомление n8n по завершении |
| `transcribe.js` | Транскрибация через Groq Whisper |
| `upload_audio.js` | Выгрузка на Яндекс.Диск (WebDAV) |
| `local_bridge.js` | Локальный мост для отладки без n8n |
| `run_join.sh` / `run_start.sh` / `run_stop.sh` | SSH-команды n8n (2 аргумента: URL + Chat ID) |
| `run_transcribe.sh` / `run_upload.sh` | Этапы обработки |
| `set_recorder_display_name.sh` | Имя бота на встрече |
| `mock_n8n.py` | Мок оркестратора для тестов |
| `database.sql` | Схема PostgreSQL |
| `docker_spec.md` | Границы ответственности контейнер/n8n |
| `services/` | Дополнительные сервисы |

## Стек

- **Node.js v20+**: Puppeteer 24, axios, groq-sdk, @aws-sdk/client-s3
- **Docker** — изолированные контейнеры записей
- **FFmpeg** — VAD (удаление тишины), сегментация по 20 мин
- **Groq** — Whisper-транскрибация (free tier) + Llama-3 базовая суммаризация
- **OpenRouter** — генерация саммари
- **n8n** — оркестрация, Telegram FSM, вебхуки
- **PostgreSQL/Supabase** — метаданные встреч
- **Яндекс.Диск WebDAV** — хранение (S3 — в планах, Milestone 3)

## База данных (database.sql)

**`meeting_transcripts`** — id, title, file_path, chat_id, transcript, summary, speaker_count, utterance_count, utterances (JSONB с таймингами), transcribed_at, operation_id (unique — защита от дублей)

**`user_settings`** — chat_id, state (FSM: IDLE...), yandex_user, yandex_webdav_password, updated_at

## Telegram UX (FSM)

- 🔴 **Запись** — режим ожидания ссылки (Force Reply), авто-подключение
- 🧠 **Аналитика/ИИ** — ручная транскрибация, саммаризация, список 5 последних встреч (с ИИ-названиями)
- ⚙️ **Настройки** — Яндекс.Диск (логин + пароль приложения) прямо из Telegram

## Стабилизация (STABILIZATION_REPORT, v0.003)

- **Docker gateway `172.19.0.1`** — SSH-нода n8n не видела `/opt/telemost-recorder` через localhost; направлять на шлюз сети `n8n_default`
- **SSH-ключ `id_rsa_n8n`** — парольная аутентификация падала (PAM/Keyboard-Interactive на Oracle Ubuntu 24.04 + fail2ban)
- **`usermod -aG docker ubuntu`** — n8n могла управлять контейнерами без sudo
- **Anti-Zombie** — `try...finally` + `browser.close()` в 100% случаев; было найдено 85 зомби-процессов Chrome
- **Webhook-First** — транскрибация стартует только после вебхука от контейнера (иначе 0-байтовые тексты)
- Скрипты принимают строго 2 аргумента (URL, Chat ID)

## Майлстоуны (ROADMAP)

| Майлстоун | Статус |
|-----------|--------|
| 1. Локальное ядро (запись + Groq-расшифровка + базовая суммаризация) | ✅ Ready (12.04.2026) |
| 2. Докеризация рекордера (Dockerfile, headless, volume `/recordings`) | 🔄 в работе |
| 3. Интеграция хранилища (S3, автозагрузка, очистка) | ⏳ |
| 4. Оркестрация через n8n (webhook, SSH/Docker, callback) | 🔄 |
| 5. Промышленная стабильность (auto-exit при тишине, логирование, длинные встречи) | ⏳ |

## Roadmap v2

- 🔴 **Diarization** — разделение реплик по спикерам
- 🔴 **Real-Time AI Chat** — вопросы боту по контексту во время записи
- 🔴 **Archival Q&A** — чат по историческим встречам с Яндекс.Диска

## Конфигурация (.env)

```ini
BOT_DISPLAY_NAME="Бот-Ассистент"
GROQ_API_KEY=gsk_...
HEADLESS=true            # true для Docker/сервера
S3_ENDPOINT/S3_REGION/S3_BUCKET/S3_ACCESS_KEY/S3_SECRET_KEY  # Milestone 3
```

## Связанное

- [[Projects/KPN-Agent/index|КПН-Агент]] — похожий пайплайн: стенограммы → саммари → реестр
- [[Synergy/Meetings/index|Расшифровки встреч]] — транскрипты совещаний
- [[Projects/index|Проекты]]
- [[AI-ML/free-ai-methods|Free-доступ: Groq, OpenRouter]]
