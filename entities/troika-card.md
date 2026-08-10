---
title: Карта Тройка — GitHub research
created: 2026-08-10
updated: 2026-08-10
type: entity
tags: [entity, transportation, nfc, rfid, security, android]
sources: [raw/articles/troika-card-github-research-2026-08-10.md]
confidence: medium
---

# Карта «Тройка» — GitHub research 🚇

**Короткий вывод:** по «Тройке» на GitHub есть несколько полезных направлений: старые Android-читалки/дамперы, парсеры транспортных карт в Metrodroid/Farebot, справочная Wiki SuperTroika, Flipper/Proxmark-экосистема для диагностики и отдельные утилиты про экономику поездок/релизы карт.

## Лучшие стартовые точки

| Репозиторий | Для чего | Чем полезен |
|---|---|---|
| [gshevtsov/TroikaDumper](https://github.com/gshevtsov/TroikaDumper) | Android-приложение для чтения/дампов карты «Тройка» | Исторический проект с прямым описанием требований: Android NFC + MIFARE Classic |
| [metrodroid/metrodroid](https://github.com/metrodroid/metrodroid) | Универсальная читалка транспортных карт | Самый содержательный код парсинга Troika: `TroikaBlock`, `TroikaTransitData`, `TroikaTrip`, `TroikaPurse`, layouts |
| [codebutler/farebot](https://github.com/codebutler/farebot) | Родственный проект чтения транспортных карт | Историческая/альтернативная реализация Troika factory |
| [InvoiceBox/wiki.supertroika.ru](https://github.com/InvoiceBox/wiki.supertroika.ru) | Wiki по SuperTroika/Troika | Справка по NFC/MIFARE, приложениям и носителям «Тройки» |
| [RfidResearchGroup/proxmark3](https://github.com/RfidResearchGroup/proxmark3) | Proxmark3/Iceman RFID/NFC tooling | Низкоуровневая диагностика и исследование MIFARE/RFID/NFC |
| [luu176/Metroflip](https://github.com/luu176/Metroflip) | Flipper Zero reader/analyzer транспортных карт | Есть `troika.c`, полезно для Flipper Zero сценариев анализа |

## Остальные найденные проекты

- [veselcraft/troika-wp](https://github.com/veselcraft/troika-wp) — Windows Phone приложение для чтения карт «Тройка».
- [WandererN/uniteTicketWriter](https://github.com/WandererN/uniteTicketWriter) — использование дешёвой московской транспортной NFC-карты как NFC-tag для бытовых данных; не про оплату поездок.
- [gridness/rustroika](https://github.com/gridness/rustroika) — калькулятор выгодного способа оплаты транспорта с «Тройкой», не NFC-парсер.
- [mycetist/troika-tracker](https://github.com/mycetist/troika-tracker) — scraper новых выпусков карт «Тройка».
- [xMasterX/all-the-plugins](https://github.com/xMasterX/all-the-plugins), [GhostESP-Revival/GhostESP](https://github.com/GhostESP-Revival/GhostESP), [DarkFlippers/unleashed-firmware](https://github.com/DarkFlippers/unleashed-firmware) — Flipper/ESP32/firmware-экосистема, где встречаются Troika/NFC/MIFARE материалы.

## Что важно технически

- «Тройка» — NFC/HF 13.56 MHz носитель; в открытых материалах часто фигурирует MIFARE / MIFARE Classic.
- Старые Android-инструменты требуют не просто NFC, а поддержку MIFARE Classic конкретным NFC-чипом.
- Metrodroid/Farebot полезны не для «накрутки», а для понимания формата транспортной карты и чтения данных.
- Proxmark3/Flipper Zero полезны как диагностические инструменты, но любые действия с балансом, билетами и клонированием требуют правового разрешения.

## Безопасная рамка

Эта заметка фиксирует исследование открытых репозиториев. Она не является инструкцией по обходу оплаты, изменению баланса или копированию транспортных носителей. Практически безопасная линия: изучать формат, читать собственную карту, использовать официальные приложения и не вмешиваться в платёжную/транспортную систему.

## Связанные заметки

- [[concepts/nfc-rfid-transport-cards|NFC/RFID транспортные карты]]
- [[entities/hermes-marketplace-tools|Marketplace MCP Server]]
- [[concepts/security|Security / безопасная рамка]]
- [[raw/articles/troika-card-github-research-2026-08-10|Raw snapshot исследования GitHub по Тройке]]
