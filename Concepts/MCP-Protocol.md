---
tags: [concept, mcp, protocol, json-rpc]
---

# MCP Protocol — базовый протокол 📡

Model Context Protocol — открытый стандарт коммуникации LLM-агентов с инструментами (Anthropic, ноябрь 2024).

## Архитектура

```
Host (Hermes/Claude Desktop)
  └─ Client ── MCP ── Server (tools/resources/prompts)
```

## Жизненный цикл

1. **initialize** — handshake: версия протокола, capabilities
2. **notifications/initialized** — подтверждение
3. **tools/list** — получить список инструментов
4. **tools/call** — вызвать инструмент с аргументами
5. **resources/read** — прочитать данные (опционально)

## Транспорты

| Транспорт | Когда |
|-----------|-------|
| **stdio** | Локальные серверы (запуск через `npx`/`uv run`) |
| **HTTP + SSE** | Удалённые серверы, веб |
| **Streamable HTTP** | Современный стандарт (2025) |

## Ключевые концепции

- **Tools** — исполняемые функции (поиск, запись, API-вызовы)
- **Resources** — данные в URI-пространстве
- **Prompts** — готовые шаблоны запросов
- **Sampling** — сервер может запросить ответ модели (обратный вызов)

## Практика

- [[AI-ML/MCP|MCP в этой базе]] — список подключённых серверов
- [[Concepts/Agentic-Systems|Агентные системы]] — как агенты используют MCP
- [[Dev/Python|Python]] — реализация MCP-серверов
