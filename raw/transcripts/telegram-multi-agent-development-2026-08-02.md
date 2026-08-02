---
source_url: telegram-mcp://search/2026-08-02-multi-agent-development
ingested: 2026-08-02
sha256: a7da4faef5c4a4a138933e2aa2f8f8bbdd4f0f244c6f857a0e7fa6c5142cb465
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
