---
title: Методология многоагентной разработки automation-проектов
created: 2026-08-02
updated: 2026-08-25
type: concept
tags: [concept, multi-agent, automation, methodology, quality-gate, security]
sources: [raw/articles/anthropic-agent-teams-2026.md, raw/articles/github-spec-kit-2026.md, raw/articles/spec-kitty-2026.md, raw/articles/swe-agent-2026.md, raw/articles/paul-agent-workflows-2026.md, raw/papers/multi-agent-software-engineering-2026.md, raw/papers/agentic-coding-evaluation-2026.md, raw/papers/agentic-software-benchmarks-2026.md, raw/articles/swebench-2026.md, raw/articles/vscode-multi-agent-development-2026.md, raw/transcripts/telegram-multi-agent-development-2026-08-02.md]
confidence: medium
---

# Методология многоагентной разработки automation-проектов

## Коротко

Методология многоагентной разработки — это не «запустить толпу агентов», а дисциплина, где каждый агент получает ограниченную роль, входные данные, артефакт на выходе и проверку качества.

## Базовый цикл

> Для Павла базовый язык процесса — GitHub Spec Kit: **project → spec → plan → tasks → implement**. Ниже этот цикл расширен под многоагентную разработку automation-проектов.

1. **Intent capture / Project** — человек формулирует бизнес-цель, проектный контекст и ограничения.
2. **Spec pass** — planner превращает намерение в спецификацию: scope, non-goals, risks, acceptance criteria.
3. **Task slicing** — architect/planner режет работу на независимые packages.
4. **Parallel execution** — implementer/researcher agents работают в изолированных контекстах.
5. **Integration** — integrator собирает изменения, разрешает конфликты, обновляет docs.
6. **Quality gates** — tester/reviewer/evaluator проверяют по рубрике и фактическим инструментам.
7. **Human review** — человек принимает решения на границах риска: деньги, прод, секреты, внешние аккаунты.
8. **Knowledge capture** — итог, источники, ошибки и паттерны уходят в [[concepts/llm-wiki|LLM Wiki]].

## Что считать артефактом

- spec.md / requirements.md
- task breakdown
- git branch/worktree или patch
- тесты и логи запуска
- security notes / permission diff
- user-facing changelog
- wiki update

## Где multi-agent оправдан

- Независимые research streams: GitHub/Web/Telegram.
- Разные специализации: backend, browser automation, security, docs.
- Проверка результата другим контекстом: reviewer/evaluator.
- Вариантный дизайн: несколько архитектурных предложений с trade-offs.

## Где multi-agent вреден

- Маленькая линейная правка.
- Нет тестов или acceptance criteria.
- Все агенты читают один и тот же огромный контекст.
- Нет владельца интеграции.
- Нет бюджета на токены/время.

## Quality gates для automation

- **Dry run** перед реальными side effects.
- **Allowlist сети и файлов** для браузерных/скрейпинговых задач.
- **Replayable tests**: сценарий можно повторить без ручного клика.
- **Rollback**: как откатить файлы, cron, config, внешние записи.
- **Evidence log**: агент показывает реальные tool outputs, а не «готово».

## Живые кейсы

- [[entities/apply-pilot|Apply Pilot]] — совместный проект поиска работы; потенциальный пример фактической агентной/spec-driven разработки с Opus/MR, где Павел участвует ресурсами, но не является владельцем методологии или продукта.


## Green Broker как второй живой кейс

[[entities/green-broker|Green Broker]] важен для методологии как проект, где Spec Kit уже применён напрямую: есть Конституция, `spec.md` и `plan.md`. В отличие от [[entities/apply-pilot|Apply Pilot]], где Павел не является владельцем процесса, Green Broker — собственный проект Павла и может стать полноценным полигоном для схемы: spec-driven вход → декомпозиция в `tasks.md` → роли агентов → quality gates → реализация.


## Связанные заметки

- [[concepts/agent-roles-for-automation|Роли агентов для automation]]
- [[concepts/spec-driven-agent-development|Spec-driven агентная разработка]]
- [[comparisons/agent-orchestration-tools|Сравнение orchestration tools]]
- [[queries/multi-agent-automation-research-plan|План исследования]]
- [[concepts/multi-agent-code-review-synergy|Мультиагентная система code review для «Синергии»]]
