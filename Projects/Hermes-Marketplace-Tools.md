---
tags: [project, mcp, marketplace, wb, ozon]
---

# Marketplace MCP Server 🛒

MCP-сервер для поиска и сравнения товаров на Wildberries и Ozon.

**Расположение:** `/home/ubuntu/hermes-marketplace-tools`

## Возможности

| Инструмент | Назначение |
|-----------|-----------|
| `marketplace_search` | Поиск товаров (query, brand, min/max price, лимит) |
| `get_product_card` | Полная карточка: характеристики, описание, изображения |
| `get_reviews` | Отзывы о товаре (сортировка: useful/recent) |

## Технические детали

- **Язык:** Python (venv: `.venv/bin/python -m mcp_server.server`)
- **Имитация браузера:** HttpClient с `impersonate="safari"` — **не** "chrome"
- **Camoufox:** `/home/ubuntu/.cache/camoufox/browsers/official/152.0.4-beta.28-3a105a2f`

## Статус площадок

| Площадка | Статус | Примечание |
|----------|--------|-----------|
| **Wildberries** | ✅ Работает | card.wb.ru отдаёт 403 на chrome, safari принимает обе точки (search + card) |
| **Ozon** | ⚠️ Блокирован | Нужен резидентский прокси (SOCKS5 109.248.203.200:1080 жив, но недостаточно) |

## Нюансы

- Павел купил **WB Клуб** — может влиять на выдачу (цены/скидки клубные)
- Для лучшего покрытия — формировать несколько запросов (с брендом и без)
- Если у маркетплейса поле `error` — площадка не ответила, пустой `items` ≠ «товаров нет»

## Связанное

- [[Dev/Python|Python]]
- [[AI-ML/MCP|MCP]]
- [[Projects/index|Проекты]]
