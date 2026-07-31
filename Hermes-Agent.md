---
tags: [hermes, ai, agent]
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

- [[Projects/Baza-Wiki|Ведение базы знаний]] (этот vault)
- [[Projects/Hermes-Marketplace-Tools|Мониторинг маркетплейсов]]
- [[Projects/KPN-Agent/index|КПН-Агент]] — контроль поручений
- Мониторинг [[AI-ML/vibecoder-sources|вайбкодерских каналов]]

## Связанное

- [[System/Hermes|Hermes — инфраструктура]]
- [[Concepts/Agentic-Systems|Агентные системы]]
- [[AI-ML/MCP|MCP]]
