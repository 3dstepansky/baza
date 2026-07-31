---
tags: [ai, mcp, protocol]
---

# MCP — Model Context Protocol 🔌

Протокол подключения инструментов и данных к LLM-агентам (Anthropic, 2024).

## Что это

Единый стандарт «USB-C для AI»: агент подключается к серверам, которые дают ему инструменты и данные.

## Компоненты

- **Host** — агент/IDE (Hermes, Claude Desktop, Cursor)
- **Client** — коннектор внутри хоста
- **Server** — предоставляет инструменты (tools), ресурсы (resources), промпты (prompts)

## Серверы в этой базе

| Сервер | Назначение |
|--------|-----------|
| **baza** (mcpvault) | Чтение/запись этого Obsidian vault |
| **telegram** (telegram-mcp) | Работа с Telegram: чтение каналов, отправка |
| **marketplace** | Парсинг Wildberries/Ozon |
| **github** | Репозитории, issues, PR |
| **hermes-admin** | Управление самим Hermes |

## Технические детали

- Транспорт: **stdio** (локальные) или **HTTP/SSE** (удалённые)
- JSON-RPC 2.0: `initialize` → `tools/list` → `tools/call`
- Инструменты монтируются в сессию агента при старте

## Ссылки

- [[AI-ML/index|AI & ML]]
- [[Concepts/MCP-Protocol|MCP Protocol — детали]]
- [[Concepts/Agentic-Systems|Агентные системы]]
- [[Projects/Hermes-Marketplace-Tools|Marketplace MCP Server]]
