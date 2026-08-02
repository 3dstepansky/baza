---
title: Spec-driven агентная разработка
created: 2026-08-02
updated: 2026-08-02
type: concept
tags: [concept, spec-driven, automation, quality-gate, github]
sources: [raw/articles/anthropic-agent-teams-2026.md, raw/articles/github-spec-kit-2026.md, raw/articles/spec-kitty-2026.md, raw/articles/swe-agent-2026.md, raw/articles/paul-agent-workflows-2026.md, raw/papers/multi-agent-software-engineering-2026.md, raw/papers/agentic-coding-evaluation-2026.md, raw/papers/agentic-software-benchmarks-2026.md, raw/articles/swebench-2026.md, raw/articles/vscode-multi-agent-development-2026.md, raw/transcripts/telegram-multi-agent-development-2026-08-02.md]
confidence: medium
---

# Spec-driven агентная разработка

## Суть

Spec-driven агентная разработка — способ заставить агентов работать не по настроению, а по контракту. До реализации создаются спецификация, план, задачи и критерии приёмки.

## Минимальный пакет spec для automation

1. **Goal** — что должно измениться в мире.
2. **Scope / non-goals** — что входит и что явно не входит.
3. **Inputs** — файлы, API, чаты, аккаунты, credentials, ограничения.
4. **Outputs** — файлы, сообщения, записи в БД, PR, аудио, отчёты.
5. **Side effects** — что может быть создано/удалено/отправлено.
6. **Acceptance criteria** — как проверить, что готово.
7. **Risks** — секреты, деньги, прод, rate limits, ban risk, prompt injection.
8. **Rollback** — как откатить.

## Как выдавать задачу агенту

Плохой prompt: «сделай Telegram→NotebookLM pipeline».

Хороший package:
- Context: ссылки на существующие файлы и ограничения DISPLAY/profile.
- Task: один узкий шаг.
- DoD: конкретный файл/лог/HTTP 200/скачанный media.
- Forbidden: не трогать config, не писать наружу, не использовать другой аккаунт.
- Report: вернуть path, command, status, failures.


## Spec Kit как общий язык проекта

Павел уже знаком с GitHub Spec Kit и его рабочей конструкцией: **project → spec → plan → tasks → implement**. Поэтому для этого исследования Spec Kit берётся не просто как один из источников, а как **понятный каркас коммуникации** между человеком, orchestrator-агентом и дочерними агентами.

### Перевод Spec Kit в многоагентную методологию

| Spec Kit слой | В многоагентной разработке | Что проверяем |
|---|---|---|
| **Project / Constitution** | правила проекта, ограничения, стек, права, стиль работы агентов | агенты не выходят за рамки проекта |
| **Spec** | контракт фичи: цель, scope, non-goals, inputs/outputs, side effects | понятно, что именно надо построить |
| **Plan** | архитектура, этапы, зависимости, выбор агентов и tool permissions | понятно, кто и в каком порядке работает |
| **Tasks** | маленькие work packages для отдельных агентов | задачи можно параллелить и ревьюить |
| **Implement** | выполнение через implementer agents + integration loop | есть код/артефакт и реальные проверки |

### Практическое правило

Если задача непонятная или большая, общаться лучше именно в терминах Spec Kit:

1. **Project:** в каком проекте/репозитории/automation-контуре работаем.
2. **Spec:** что должно получиться и что не делаем.
3. **Plan:** как разложить на роли агентов и этапы.
4. **Tasks:** какие независимые пакеты можно отдать субагентам.
5. **Implement:** что реально запускаем, проверяем и коммитим.

Это делает многоагентность понятнее: не «толпа агентов что-то делает», а Spec Kit pipeline, где каждый слой порождает проверяемые артефакты.


## Живые кейсы

- [[entities/apply-pilot|Apply Pilot]] — внешний/совместный проект поиска работы, который используется как пример анализа уже случившейся LLM-разработки.
- [[entities/green-broker|Green Broker]] — реальный проект Павла по Telegram-боту для продажи растений, уже оформленный в формате Constitution → Spec → Plan и подходящий для дальнейшего разбиения в `tasks.md`.

## Почему это важно

Spec-driven подход превращает vibe-coding в инженерный процесс. Агентам проще параллелиться, reviewer понимает что проверять, а человек видит риски до запуска.

## Связанные заметки

- [[concepts/multi-agent-development-methodology|Методология многоагентной разработки]]
- [[concepts/kpn-requirements|Контроль поручений — требования]]
- [[comparisons/agent-orchestration-tools|Сравнение orchestration tools]]
- [[queries/multi-agent-automation-research-plan|План исследования]]
