---title: "MCP — Model Context Protocol 🔌"
type: concept

tags: [ai, mcp, protocol]
created: 2026-07-30
updated: 2026-08-17
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
| [[entities/construction-maps-mcp|construction-maps-mcp]] | Кадастр, полигоны, Росреестр/НСПД + Yandex Maps |
| [[queries/russian-grocery-mcp-research-plan|russian-grocery-mcp-research-plan]] | План исследования MCP-адаптеров для Самоката, Пятёрочки, Перекрёстка, Ленты, Магнита, Красного и Белого, Евроспара |
| **yougile** (`@nebelov/yougile-mcp`) | YouGile API v2: проекты, доски, колонки, задачи; используется для [[entities/lushertale|LusherTale / ПсихоСказка]] |

## Технические детали

- Транспорт: **stdio** (локальные) или **HTTP/SSE** (удалённые)
- JSON-RPC 2.0: `initialize` → `tools/list` → `tools/call`
- Инструменты монтируются в сессию агента при старте

## Ссылки

- [[index|AI & ML]]
- [[concepts/mcp-protocol|MCP Protocol — детали]]
- [[concepts/agentic-systems|Агентные системы]]
- [[entities/hermes-marketplace-tools|Marketplace MCP Server]]
- [[entities/lushertale|LusherTale / ПсихоСказка]]
- [[queries/russian-grocery-mcp-research-plan|Российские grocery-приложения и MCP-серверы]]
