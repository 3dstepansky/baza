---
source_url: "github-search:troika-card-2026-08-10"
ingested: 2026-08-10
sha256: 6901c533ee063575e0eaaf54ea5237006df0c814d930da907e588018c29bc4ce
title: "GitHub research snapshot — карта Тройка"
---

# GitHub research snapshot — карта «Тройка» / Troika card

Дата исследования: 2026-08-10
Запрос: «поищи на GitHub репозитории посвященные карте 3йка»
Метод: GitHub MCP repository/code search по запросам `troika-card`, `Troika card`, `тройка MIFARE`, `troika mifare`, `Moscow transport card`, `Troika NFC`.

## Найденные репозитории и материалы

| Репозиторий | Назначение | Практическая ценность |
|---|---|---|
| https://github.com/gshevtsov/TroikaDumper | Android-приложение для чтения, сохранения и восстановления дампа памяти карты «Тройка» | Исторически важная утилита и README с требованиями к Android/NFC/MIFARE Classic |
| https://github.com/metrodroid/metrodroid | Большой проект для чтения транспортных карт через NFC; содержит пакет `transit/troika` | Лучший открытый источник по парсингу структуры данных «Тройки» |
| https://github.com/codebutler/farebot | Родственный/предшествующий проект чтения транспортных карт | Полезен как исторический код и альтернативная реализация Troika factory |
| https://github.com/InvoiceBox/wiki.supertroika.ru | Wiki по SuperTroika / Troika, включая страницу про NFC | Справочный источник по NFC, MIFARE и приложениям для записи билетов |
| https://github.com/veselcraft/troika-wp | Windows Phone приложение для чтения карт «Тройка» | Историческая реализация для Windows Phone |
| https://github.com/WandererN/uniteTicketWriter | Android-приложение: использовать дешёвую московскую транспортную NFC-карту как NFC-tag | Не про оплату поездок, а про запись бытовых NFC-данных в свободные области |
| https://github.com/gridness/rustroika | Расчёт выгодного способа оплаты транспорта с «Тройкой» | Полезно для экономики поездок, не для NFC-анализа |
| https://github.com/mycetist/troika-tracker | Web scraper для отслеживания новых выпусков карт «Тройка» | Полезно коллекционерам и для мониторинга релизов носителей |
| https://github.com/RfidResearchGroup/proxmark3 | Основной инструмент Proxmark3/Iceman для RFID/NFC-исследований | Низкоуровневая диагностика LF/HF/RFID/NFC; в поиске встречаются MIFARE/Troika ключевые материалы |
| https://github.com/luu176/Metroflip | Flipper Zero приложение для чтения/анализа транспортных карт | Есть `troika.c`, полезно для Flipper Zero сценариев диагностики |
| https://github.com/xMasterX/all-the-plugins | Сборник Flipper-плагинов | Внутри встречается Metroflip/Troika parser |
| https://github.com/GhostESP-Revival/GhostESP | ESP32-платформа, в коде найден `troika.c` | Экспериментальная среда; полезна как пример парсера, не как основной источник |
| https://github.com/DarkFlippers/unleashed-firmware | Кастомная прошивка Flipper Zero | В поиске встречаются Troika/NFC материалы и словари MIFARE |

## Технические факты из найденных материалов

- «Тройка» относится к NFC/HF 13.56 MHz носителям и в открытых материалах часто описывается через MIFARE / MIFARE Classic.
- Не каждый Android-телефон с NFC подходит: для части старых инструментов нужен NFC-чип с поддержкой MIFARE Classic; Broadcom/часть других чипов могут не работать.
- Metrodroid содержит отдельный пакет Troika parser с файлами `TroikaBlock.kt`, `TroikaTransitData.kt`, `TroikaTrip.kt`, `TroikaPurse*`, `TroikaLayout*`.
- SuperTroika Wiki утверждает, что в «Тройке» используется Mifare-чип, а билеты и абонементы записываются на NFC-носитель.
- Для безопасной диагностики полезны читатели/инструменты уровня Android NFC, Proxmark3, Flipper Zero, но действия с оплатой/балансом требуют строгого соблюдения закона и правил перевозчика.

## Ограничения и безопасность

- В найденных старых README встречаются разделы про запись дампов/изменение состояния карты. Эти сведения сохранены только как факт существования репозиториев, без процедур и инструкций.
- Практическое использование таких материалов может нарушать правила перевозчика и закон, если направлено на обход оплаты, изменение баланса или клонирование чужих/служебных носителей.
- Безопасная линия: изучать формат, читать собственную карту, анализировать публичный код, использовать официальные приложения для покупки/записи билетов.
