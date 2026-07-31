---
tags: [dev, python, language]
---

# Python 🐍

Основной язык для AI/ML, автоматизации и MCP-серверов в этой базе знаний.

## Когда использовать

- **AI/ML**: инференс, работа с моделями, prompt engineering
- **MCP-серверы**: большинство серверов (marketplace, telegram) написаны на Python
- **Автоматизация**: скрипты, парсинг, ETL
- **Асинхронность**: `asyncio` для параллельных задач (например, массовый сбор данных)

## Ключевые инструменты

| Инструмент | Назначение |
|-----------|-----------|
| **uv** | Менеджер пакетов и окружений (быстрее pip/poetry) |
| **FastAPI** | Веб-API и MCP-серверы |
| **pandas** | Анализ данных, таблицы |
| **httpx** | HTTP-клиент с impersonate (safari/chrome) — критично для маркетплейсов |

## Практика в проектах

- [[Projects/Hermes-Marketplace-Tools|Marketplace MCP Server]] — Python + camoufox + impersonate
- [[Concepts/MCP-Protocol|MCP Protocol]] — реализация серверов на Python
- [[AI-ML/Local-LLM|Локальные LLM]] — запуск Ollama через Python API

## Ссылки

- [[Dev/index|Разработка]]
- [[Concepts/Agentic-Systems|Агентные системы]]
