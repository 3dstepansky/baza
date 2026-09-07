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
- [[concepts/helios-intake-agent-forge-and-commissioning-lifecycle|Временный агент-пусконаладчик (Ephemeral Commissioning Agent) в среде «Гелиос»]] — десантирование в Docker на ПК сотрудника, устранение технической неопределенности, настройка окружения и последующее самоудаление после сдачи процесса «под ключ».
- [[entities/hermes-marketplace-tools|Мониторинг маркетплейсов]]
- [[index|КПН-Агент]] — контроль поручений
- Мониторинг [[entities/vibecoder-sources|вайбкодерских каналов]]

## Связанное

- [[entities/helios-agent-environment|Агентская среда «Гелиос»]]
- [[concepts/helios-intake-agent-forge-and-commissioning-lifecycle|Жизненный цикл агентов и Гермес-пусконаладчик]]
- [[entities/hermes|Hermes — инфраструктура]]
- [[concepts/agentic-systems|Агентные системы]]
- [[concepts/mcp|MCP]]
