---
title: Сравнение подходов к orchestration coding agents
created: 2026-08-02
updated: 2026-08-02
type: comparison
tags: [comparison, multi-agent, orchestration, claude-code, codex, github, benchmark]
sources: [raw/articles/anthropic-agent-teams-2026.md, raw/articles/github-spec-kit-2026.md, raw/articles/spec-kitty-2026.md, raw/articles/swe-agent-2026.md, raw/articles/paul-agent-workflows-2026.md, raw/papers/multi-agent-software-engineering-2026.md, raw/papers/agentic-coding-evaluation-2026.md, raw/papers/agentic-software-benchmarks-2026.md, raw/articles/swebench-2026.md, raw/articles/vscode-multi-agent-development-2026.md, raw/transcripts/telegram-multi-agent-development-2026-08-02.md]
confidence: medium
---

# Сравнение подходов к orchestration coding agents

## Что сравниваем

Подходы к организации нескольких AI-агентов в разработке: Claude Code subagents/agent teams, GitHub/Copilot fleet-like запуск, SWE-agent harness, LangChain evaluator/rubric loop, Agent Mesh / orchestration frameworks, custom CLI orchestrators.

## Быстрое сравнение

| Подход | Сильная сторона | Главный риск |
|---|---|---|
| Claude Code subagents | Изолированные контексты, роли, tools/permissions | Стоимость/effort дочерних агентов и ручная дисциплина |
| Spec Kit / Spec Kitty | Контракт до кода, понятные tasks | Можно бюрократизировать маленькие задачи |
| SWE-agent style harness | Issue → patch → tests, воспроизводимость | Требует test harness и окружения |
| Rubric/evaluator loop | Проверка по критериям до финала | Evaluator тоже может ошибаться без factual tools |
| Agent Mesh / frameworks | События, интеграции, production orchestration | Overengineering для локального вайбкодинга |
| Custom CLI orchestrator | Можно смешивать Claude/Codex/Copilot/Gemini | Хрупкость, секреты, разные форматы контекста |

## Предварительный вывод

Для Павла и automation-проектов оптимальна гибридная схема:

- **Spec-driven вход** — чтобы не хаотить.
- **Claude/Hermes-style orchestrator** — держит todo, tools, память и wiki.
- **2–4 специализированных агента** на независимых work packages.
- **Evaluator/reviewer** по рубрике.
- **Git/worktree discipline** для параллельных правок.
- **LLM Wiki capture** после каждого нетривиального проекта.

## Связанные заметки

- [[concepts/multi-agent-development-methodology|Методология многоагентной разработки]]
- [[concepts/agent-roles-for-automation|Роли агентов для automation]]
- [[concepts/spec-driven-agent-development|Spec-driven агентная разработка]]
- [[concepts/agentic-systems|Агентные системы]]
