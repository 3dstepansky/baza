---
title: Apply Pilot — проект поиска работы
created: 2026-08-02
updated: 2026-08-02
type: entity
tags: [entity, project, job-search, automation, agent, multi-agent, spec-driven]
sources: [raw/transcripts/apply-pilot-context-2026-08-02.md]
confidence: medium
---

# Apply Pilot — проект поиска работы

## Суть

**Apply Pilot** — проект по поиску работы, который Павел ведёт вместе с ещё одним программистом. По словам Павла, проект уже содержит практические наработки, похожие на [[concepts/multi-agent-development-methodology|многоагентную разработку automation-проектов]]: промпты, доработки, агентоподобное разделение работы и MR, собранный Opus. ^[raw/transcripts/apply-pilot-context-2026-08-02.md]

## Роль Павла

Важное ограничение контекста: Павел **не является инициатором, методологическим владельцем и продуктовым владельцем** этого проекта. Он выступал своими ресурсами и знает часть проекта, но не владеет им в полной мере. Поэтому Apply Pilot нужно рассматривать как **внешний/совместный живой кейс**, а не как полностью управляемый Павлом проект. ^[raw/transcripts/apply-pilot-context-2026-08-02.md]

## Почему важен для исследования

Apply Pilot — потенциально сильный case study для нашей методологии:

- домен понятный: поиск работы и автоматизация откликов;
- уже есть реальные MR/код/промпты;
- разработка частично шла с LLM/Opus;
- есть признаки [[concepts/spec-driven-agent-development|spec-driven агентной разработки]], но методология, судя по описанию, не оформлена явно;
- можно сравнить фактический процесс с каркасом **project → spec → plan → tasks → implement**.

## Как разбирать Apply Pilot

Когда появится доступ к MR/репозиторию/patch, разбор делать не просто как code review, а по схеме:

1. **Project** — кто владелец, какие цели, ограничения, стек, зоны ответственности.
2. **Spec** — какая фича или изменение требовались.
3. **Plan** — как Opus/разработчики разложили работу.
4. **Tasks** — какие отдельные work packages видны в diff/commit history.
5. **Implement** — что реально вошло в MR.
6. **Review / QA** — какие тесты, CI, human review, security checks были или отсутствовали.
7. **Lessons** — какие паттерны перенести в [[concepts/multi-agent-development-methodology|методологию многоагентной разработки]].

## Открытые вопросы

- Какие именно промпты используются в проекте?
- Есть ли `spec/plan/tasks` артефакты или они живут только в переписке/промптах?
- Какой стек проекта и какие внешние сервисы задействованы?
- Что именно сделал MR `!653`, собранный Opus?
- Какие quality gates сейчас есть: tests, CI, review, ручные проверки?
- Где граница ответственности Павла, второго программиста и AI-агентов?

## Связанные заметки

- [[concepts/spec-driven-agent-development|Spec-driven агентная разработка]]
- [[concepts/multi-agent-development-methodology|Методология многоагентной разработки automation-проектов]]
- [[concepts/agent-roles-for-automation|Роли агентов для automation-проектов]]
- [[entities/job-search|job_search]]
