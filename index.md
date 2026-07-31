---
tags: [hub, index]
---

# Baza — LLM Wiki 🧠

Персональная база знаний, управляемая через [[Hermes-Agent|Hermes Agent]].

## Разделы

### Разработка
- [[Dev/index|Разработка]] — проекты, тулы, языки, практики
- [[Dev/Python|Python]] — основной язык AI/ML и автоматизации
- [[Dev/Go|Go]] — системный язык

### AI / ML
- [[AI-ML/index|AI & ML]] — модели, MCP, исследования, free-tier
- [[AI-ML/omniroute|OmniRoute]] — локальный AI-прокси (271 провайдер)
- [[AI-ML/Local-LLM|Локальные LLM]] — Ollama, GGUF, квантование
- [[AI-ML/MCP|MCP]] — Model Context Protocol
- [[AI-ML/vibecoder-sources|Вайбкодерские источники]] — Telegram-каналы для мониторинга

### Трейдинг
- [[Trading/index|Трейдинг]] — алгоритмы, стратегии, боты
- [[Trading/Algo|Алгоритмическая торговля]]

### Система
- [[System/index|Система]] — серверы, сеть, прокси
- [[System/Hermes|Hermes Agent]] — инфраструктура платформы

### Концепции
- [[Concepts/index|Концепции]] — Karpathy-style заметки
- [[Concepts/LLM-Wiki|LLM Wiki]] — как устроена эта база
- [[Concepts/Agentic-Systems|Агентные системы]]

### Проекты
- [[Projects/index|Проекты]] — активные проекты и идеи
- [[Projects/Baza-Wiki|Baza Wiki]] — этот проект

### Холдинг
- [[Synergy/index|Синергия]] — оргструктура, встречи, проекты

См. также: [[README|README базы]]

## Как работать с базой

1. **Сохранить** — «это в базу» → заметка по теме
2. **Найти** — поиск по vault (MCP baza)
3. **Расширить** — новые каналы/источники добавляются в [[AI-ML/vibecoder-sources|список]]
4. **Опубликовать** — статический сайт `_site/` + граф связей

## Последние заметки
```dataview
LIST
FROM ""
SORT file.mtime DESC
LIMIT 10
```
