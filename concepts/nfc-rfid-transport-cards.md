---
title: NFC/RFID транспортные карты
created: 2026-08-10
updated: 2026-08-10
type: concept
tags: [concept, transportation, nfc, rfid, security]
sources: [raw/articles/troika-card-github-research-2026-08-10.md]
confidence: medium
---

# NFC/RFID транспортные карты 🪪

**Суть:** транспортные карты вроде московской «Тройки» — это NFC/HF 13.56 MHz носители, где данные билетов/абонементов читаются и записываются через совместимые считыватели. Открытые GitHub-проекты помогают понять формат и инструменты чтения, но не отменяют правовые ограничения.

## Практические классы инструментов

| Класс | Примеры | Для чего полезен |
|---|---|---|
| Android NFC apps | TroikaDumper, Metrodroid, Farebot | Чтение и разбор транспортных карт на совместимых телефонах |
| Proxmark3 | RfidResearchGroup/proxmark3 | Низкоуровневая диагностика RFID/NFC, исследование MIFARE |
| Flipper Zero apps | Metroflip, plugin packs | Портативное чтение/анализ форматов транспортных карт |
| Справочные wiki | SuperTroika Wiki | Понимание NFC, MIFARE и пользовательских приложений |

## Ограничения

- Наличие NFC в телефоне не означает поддержку MIFARE Classic.
- Для старых Android-инструментов важен производитель NFC-чипа.
- Открытый код может быть устаревшим и не отражать текущую инфраструктуру транспорта.
- Чтение собственной карты и исследование формата отличается от вмешательства в оплату/баланс.

## Связанные заметки

- [[entities/troika-card|Карта Тройка — GitHub research]]
- [[concepts/security|Security / безопасная рамка]]
- [[entities/hermes|Hermes Agent — инфраструктура]]
- [[raw/articles/troika-card-github-research-2026-08-10|Raw snapshot исследования GitHub по Тройке]]
