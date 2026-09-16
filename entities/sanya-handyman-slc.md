---
title: "Саня — Handyman в Солт-Лейк-Сити (США) и стек лидогенерации"
type: entity
tags:
  - handyman
  - salt-lake-city
  - usa
  - lead-generation
  - real-estate
date: 2026-09-11
---

# Саня (Handyman в Salt Lake City, Utah)

Саня — друг Павла, развивающий бизнес по мелкому бытовому ремонту (Handyman Services) в Солт-Лейк-Сити и округе Salt Lake County, штат Юта, США.

## Специфика рынка и позиционирование
- **Локальный контекст:** Культ семейных домов (2,500–4,500 sqft), жесткая горная вода, сезонное обслуживание (sprinkler winterization, террасы, водостоки).
- **Ключевой B2B канал:** Риелторы, закрывающие сделки купли-продажи (потребность в устранении замечаний инспекции — Inspection Punch Lists, подготовка к продаже — Pre-listing repairs, пакеты въезда для покупателей).
- **Русскоязычные риелторы:** Сильное комьюнити (Slavic Community / Utah Russian Network), приоритетный теплый канал контакта.

## Автоматизированный стек лидогенерации
Развернут в Docker на сервере в `/home/ubuntu/slc-handyman-leads/`:
- **Источник данных:** MLS / HomeHarvest + Salt Lake County ArcGIS Open Data.
- **Периодичность:** Ежедневный / еженедельный парсинг свежих закрытых сделок (last 7–30 days).
- **Выходные артефакты:** 
  - База B2B контактов риелторов с телефонами и готовыми SMS/Email скриптами.
  - База адресов новосёлов для локального директ-маркетинга.
  - Excel-отчет: `/home/ubuntu/slc-handyman-leads/data/SLC_Handyman_Deals_LATEST.xlsx`.
