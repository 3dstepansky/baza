---
title: Агентская среда «Гелиос» (Helios Agent Environment)
tags: [helios, agents, multi-agent, architecture, synergy]
type: entity
created: 2026-09-07
updated: 2026-09-07
---

# Агентская среда «Гелиос» (Helios Agent Environment)

> Платформа и среда для генерации, конфигурирования, развертывания и контекстной оркестрации AI-агентов, автоматизирующих операции и сквозные бизнес-процессы в корпорации.

---

## 🎯 Концепция и назначение

«Гелиос» решает две ключевые задачи:
1. **Генерация и конфигурирование агентов:** Создание специализированных AI-агентов под конкретные роли и функции компании.
2. **Операционное исполнение и синергия:** Оркестрация взаимодействия агентов между собой, с сотрудниками-людьми и с корпоративными IT-системами (1C, CRM, ERP, базы данных).

---

## 🧩 Архитектурный фундамент: C4 + Architecture as Code

Для того чтобы агенты работали контекстуально обусловлено (в рамках структуры корпорации, регламентов, доступов и правил), «Гелиос» опирается на методологию [[concepts/c4-model-for-business-and-agents|C4 Model и Architecture as Code]]:

* **Единый источник контекста (Single Source of Truth):** Архитектура бизнеса и связи между агентами описываются в виде машиночитаемых YAML-манифестов в Git-репозитории.
* **Семантический зум (Google Maps Zoom):**
  * **C1 (Context):** Внешний контур компании и ключевые стейкхолдеры.
  * **C2 (Containers):** Департаменты и бизнес-домены (Продажи, Склад, Бухгалтерия, HR).
  * **C3 (Components):** Роли агентов, сотрудников и микросервисов.
  * **C4 (Code/Prompts):** Промпты, MCP-тулы, схемы валидации и системные инструкции.
* **Формирование базы из оргструктуры:** Загрузка штатного расписания для построения «1-го уровня наивности» — первоначального интерактивного графа всей компании, на который затем приземляются агенты.

---

## ⚙️ Структура манифеста агента в «Гелиосе» (Пример C3)

```yaml
id: helios.sales.lead_qualifier
type: agent
level: C3
title: "Агент квалификации лидов"
department: sales_department

context:
  goal: "Первичный скоринг заявок из Telegram и сайта, обогащение контактов"
  inputs:
    - from: helios.external.telegram_inbox
      contract: LeadPayloadSchema
  outputs:
    - to: helios.sales.crm_sync_agent
      condition: "score >= 70"
    - to: human.sales.manager
      condition: "score < 70 or requires_call"

capabilities:
  tools:
    - mcp: "crm-tools"
      allow: ["search_lead", "update_status"]
    - mcp: "telegram-tools"
      allow: ["send_message"]
```

---

## 🔗 Связанные материалы
* [[concepts/c4-model-for-business-and-agents|C4 Model и Architecture as Code для описания бизнеса и агентов]]
* [[raw/transcripts/archdays-2022-arch-repo-c4-vetchinkin|Конспект доклада Ветчинкина на ArchDays 2022]]
* [[concepts/agentic-systems|Агентские системы]]
* [[concepts/multi-agent-development-methodology|Методология многоагентной разработки]]
* [[entities/hermes-agent|Платформа Hermes Agent]]
