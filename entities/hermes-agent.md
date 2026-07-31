---title: "Hermes Agent — Платформа агентов 🧬"
type: entity

tags: [hermes, ai, agent]
created: 2026-07-30
updated: 2026-07-31
---


# Hermes Agent — Платформа агентов 🧬

AI-агентная платформа от Nous Research, работающая через Telegram и веб.

## Возможности

- **Мультиплатформенность**: Telegram, веб, локальные файлы
- **MCP-интеграции**: 100+ серверов (Obsidian, GitHub, маркетплейсы, Telegram)
- **Делегирование**: параллельные субагенты с изолированным контекстом
- **Память**: долговременная (memories) + переиспользуемые skills
- **Автоматизация**: cron-задачи, канбан-оркестрация
- **Мультимодальность**: голосовые (TTS/STT), изображения, медиа

## Архитектура

```
Telegram/Web
    ↓
 Hermes Gateway
    ↓
 Agent core (LLM: OmniRoute/OpenRouter)
    ↓
 MCP tools + Skills + Memory + Cron
```

## Для чего используется здесь

- [[entities/baza-wiki|Ведение базы знаний]] (этот vault)
- [[entities/hermes-marketplace-tools|Мониторинг маркетплейсов]]
- [[index|КПН-Агент]] — контроль поручений
- Мониторинг [[entities/vibecoder-sources|вайбкодерских каналов]]

## Связанное

- [[entities/hermes|Hermes — инфраструктура]]
- [[concepts/agentic-systems|Агентные системы]]
- [[concepts/mcp|MCP]]
