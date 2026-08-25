---
title: Роли агентов для automation-проектов
created: 2026-08-02
updated: 2026-08-25
type: concept
tags: [concept, agent, multi-agent, automation, orchestration]
sources: [raw/articles/anthropic-agent-teams-2026.md, raw/articles/github-spec-kit-2026.md, raw/articles/spec-kitty-2026.md, raw/articles/swe-agent-2026.md, raw/articles/paul-agent-workflows-2026.md, raw/papers/multi-agent-software-engineering-2026.md, raw/papers/agentic-coding-evaluation-2026.md, raw/papers/agentic-software-benchmarks-2026.md, raw/articles/swebench-2026.md, raw/articles/vscode-multi-agent-development-2026.md, raw/transcripts/telegram-multi-agent-development-2026-08-02.md]
confidence: medium
---

# Роли агентов для automation-проектов

## Ролевая модель

### 1. Orchestrator / Lead

Держит цель, ограничения, todo, зависимости и принимает решение, кого запускать. Не должен сам тонуть в деталях каждого источника.

### 2. Researcher

Собирает источники по одному направлению: GitHub, Web/arXiv, Telegram, docs. Возвращает краткий structured digest + ссылки + уровень уверенности.

### 3. Spec Writer

Преобразует хаотичное желание в spec: scope, non-goals, acceptance criteria, данные, права, side effects.

### 4. Architect

Выбирает архитектуру, границы модулей, интерфейсы, хранение состояния, retries, idempotency, rollback.

### 5. Implementer

Пишет код в изолированной ветке/worktree. На вход получает маленький task package, а не «сделай всё».

### 6. Tester / QA

Создаёт и запускает проверки: unit, integration, browser, API, smoke. Его результат — фактический лог.

### 7. Security / Risk Reviewer

Проверяет secrets, prompt injection, file/network permissions, внешние аккаунты, irreversible actions.

### 8. Evaluator / Rubric Grader

Сравнивает результат с rubric/Definition of Done. Может возвращать задачу implementer на доработку.

### 9. Documenter / Wiki Curator

Обновляет README, changelog, runbook и [[concepts/llm-wiki|LLM Wiki]]. Фиксирует решения, pitfalls и источники.

## Практическое правило

Один агент = один тип ответственности. Если агент одновременно исследует, пишет код, проверяет и документирует — это single-agent workflow с иллюзией команды.

## Связанные заметки

- [[concepts/multi-agent-development-methodology|Методология многоагентной разработки]]
- [[concepts/agentic-systems|Агентные системы]]
- [[entities/hermes-agent|Hermes Agent]]
- [[concepts/mcp|MCP]]
- [[concepts/multi-agent-code-review-synergy|Мультиагентная система code review для «Синергии»]]
