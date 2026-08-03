---
source_url: telegram-mcp://search/2026-08-02-multi-agent-development
ingested: 2026-08-02
sha256: b499395c852270fdcdaa337246645ee2a38d9e18f1797fddbd1c88525a9485a0
---

# Telegram: multi-agent / Claude Code / vibe-coding snippets

Срез Telegram-обсуждений по теме многоагентной разработки, Claude Code, subagents, orchestration и вайбкодинга.

Найденные сигналы:
- В обсуждениях активно всплывает оркестрация CLI-агентов: operator/advisor/worker, разные модели под разные роли, вызов Codex/Claude Code/Copilot/Grok/Pi через общий orchestrator.
- Claude Code subagents воспринимаются как практичный слой: интерфейс, permissions, tools и изолированные окна, а модель может быть заменена через proxy/CLI обвязку.
- Есть практический риск: у дочерних агентов могут наследоваться дорогие effort/лимиты; роль/модель/effort нужно задавать явно.
- LangChain RubricMiddleware подтверждает тренд на выделенного evaluator/grader агента, который проверяет результат по рубрике и возвращает задачу на доработку.
- В русскоязычном вайбкодинге сильный фокус на automation и бизнес-системы: ERP, сметчики, Telegram-боты для сотрудников, n8n/MCP/Claude Code.
- Важная security-линия: prompt injection в чужих источниках, sandbox/network/file limits, снижение approval fatigue.

Релевантные сообщения: @big_llm_course про ERP и итерационный вайбкодинг; @GitHub_Projects_Daily про agent governance, Solace Agent Mesh, Copilot fleet, background agents; обсуждения Claude Code subagents и RubricMiddleware.
