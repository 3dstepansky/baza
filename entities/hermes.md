---title: "Hermes Agent — инфраструктура 🛠️"
type: entity

tags: [system, hermes, infra]
created: 2026-07-30
updated: 2026-07-31
---


# Hermes Agent — инфраструктура 🛠️

Локально-управляемая AI-платформа (Nous Research), работающая на сервере.

## Компоненты

| Компонент | Назначение |
|-----------|-----------|
| **Gateway** | Telegram-мост, приём/отправка сообщений |
| **Dashboard** | Веб-UI + REST API (порт 9119) |
| **MCP-серверы** | Инструменты: baza, telegram, marketplace, github |
| **Cron** | Планировщик периодических задач |
| **Kanban** | Очереди задач для агентов |
| **Memories** | Долговременная память (MEMORY.md, USER.md) |
| **Skills** | Переиспользуемые инструкции в `~/.hermes/skills/` |

## Полезные команды

```bash
hermes gateway restart      # перезапуск (подхват новых MCP)
hermes config set <key> <v> # настройка
hermes mcp list             # список MCP-серверов
hermes serve                # dashboard на :9119
```

## Профили

- Профили = отдельные агенты (свои skills/memories/cron)
- Активный: **default**

## Связанное

- [[index|Система]]
- [[concepts/agentic-systems|Агентные системы]]
- [[entities/hermes-agent|Hermes Agent — платформа]]
- [[index|КПН-Агент на базе Hermes]]
