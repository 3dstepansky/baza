---
title: Исследовательский проект: методология многоагентной разработки automation-проектов
created: 2026-08-02
updated: 2026-08-02
type: query
tags: [query, multi-agent, automation, methodology, github, telegram]
sources: [raw/articles/anthropic-agent-teams-2026.md, raw/articles/github-spec-kit-2026.md, raw/articles/spec-kitty-2026.md, raw/articles/swe-agent-2026.md, raw/articles/paul-agent-workflows-2026.md, raw/papers/multi-agent-software-engineering-2026.md, raw/papers/agentic-coding-evaluation-2026.md, raw/papers/agentic-software-benchmarks-2026.md, raw/articles/swebench-2026.md, raw/articles/vscode-multi-agent-development-2026.md, raw/transcripts/telegram-multi-agent-development-2026-08-02.md]
confidence: medium
---

# Исследовательский проект: методология многоагентной разработки automation-проектов

## Цель

Построить прикладную методологию многоагентной разработки для automation-проектов: от идеи и источников до работающего артефакта, тестов, документации и наставнического подкаста.

## Исследовательский pipeline

1. **Raw sources** — GitHub, Web/arXiv, Telegram сохраняются в `raw/` как неизменяемые источники.
2. **Wiki layer** — из источников создаются страницы: [[concepts/multi-agent-development-methodology|методология]], [[concepts/agent-roles-for-automation|роли агентов]], [[concepts/spec-driven-agent-development|spec-driven workflow]], [[comparisons/agent-orchestration-tools|сравнение инструментов]].
3. **Synthesis** — сборка практического playbook: фазы, роли, артефакты, quality gates, git/worktree, human review.
4. **NotebookLM** — после стабилизации wiki-материалов подготовить наставнический сценарий и аудиоподкаст.

## Гипотеза

Многоагентность полезна не количеством агентов, а **управляемым разделением труда**: отдельные контексты, независимые задачи, проверяемые артефакты, evaluator/reviewer loop и человек как владелец решений.

## Основные вопросы

- Какие роли нужны именно для automation-проектов, а не абстрактного SWE?
- Где агентам давать параллельность, а где нужен последовательный контроль?
- Какой минимальный набор specs нужен перед запуском implementation agents?
- Какие quality gates обязательны: tests, browser checks, lint, security, rollback?
- Как не сжечь токены на бессмысленной оркестрации?

## Связанные заметки

- [[concepts/agentic-systems|Агентные системы]]
- [[concepts/mcp|MCP]]
- [[entities/vibecoder-sources|Вайбкодерские источники]]
- [[entities/hermes-agent|Hermes Agent]]
