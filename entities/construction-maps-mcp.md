---
title: Construction Maps MCP Server — кадастр и полигоны
created: 2026-08-09
updated: 2026-08-09
type: entity
tags: [entity, mcp, api, python, automation, tool]
sources: [raw/articles/construction-maps-mcp-repository-2026-08-09.md]
confidence: medium
---

# Construction Maps MCP Server — кадастр и полигоны

**Construction Maps MCP Server** — Python MCP-сервер для предпроектного анализа земельных участков: кадастровые границы/полигоны через Росреестр/НСПД и картографический слой через Yandex Maps.^[raw/articles/construction-maps-mcp-repository-2026-08-09.md]

## Почему сохранён

Павел отметил его после подкаста как отдельный сервер под будущую автоматизацию: **кадастровые карты, границы участков и полигоны**. Это не основной универсальный Yandex Maps MCP, а специализированный строительный/земельный слой.

## Репозиторий и статус

| Поле | Значение |
|---|---|
| Репозиторий | https://github.com/alexgrebeshok-coder/construction-maps-mcp |
| Назначение | Анализ земельных участков в строительстве |
| Интеграции | Росреестр/НСПД + Yandex Maps |
| Язык | Python |
| Версия из README/pyproject | 1.0.0 |
| Последний observed commit main | `3b1b258ddcceaeb090460e739a882d4f7422b330`, 2026-07-05 |
| Latest pushed_at по GitHub API | 2026-07-19T05:26:04Z |
| License | README/pyproject: MIT; GitHub API license field: null |
| Confidence | medium: источник один репозиторий, код ещё нужно тестировать перед production |

## Ключевые возможности

### Кадастр

- `cadastre_get_boundaries` — получить границы участка по кадастровому номеру в GeoJSON.
- `cadastre_get_info` — получить площадь, адрес и категорию участка.
- `cadastre_search_by_address` — найти участки по адресу.

### Полигоны и геометрия

- `geometry_calculate_area` — рассчитать площадь полигона.
- `geometry_check_intersection` — проверить пересечение участков/полигонов.
- `geometry_measure_distance` — измерить расстояние между точками.
- `geometry_buffer` — построить буфер вокруг геометрии.

### Карты и инфраструктура

- `geocode_address_to_coords` / `geocode_coords_to_address` — связка адресов и координат.
- `infrastructure_find_nearby` — школы, больницы, АЗС и другие объекты рядом с участком.
- `infrastructure_calculate_distances` — расстояния до поставщиков/объектов.
- `infrastructure_get_satellite_image` — спутниковый снимок участка.
- `visualization_generate_static_map`, `visualization_export_geojson`, `export_to_json` — карта, GeoJSON и JSON-выгрузка.

## Архитектура

- MCP SDK для подключения к агентам.
- `rosreestr2coord` для кадастровых данных/НСПД.
- Yandex Maps API для геокодирования, карт и снимков.
- `shapely`/`geomet` для геометрических операций.
- Двухуровневый кеш: in-memory + SQLite.
- Rate limiting и backoff для Yandex/Rosreestr API.

## Требования для будущей автоматизации

- Python 3.10+.
- Yandex Maps API key в окружении `YANDEX_MAPS_API_KEY`.
- Не хранить ключ в заметках или публичных конфигурациях.
- Перед подключением к Hermes протестировать реальные calls на 1–2 кадастровых номерах и проверить, что `rosreestr2coord` ещё работает с текущим НСПД.

## Черновая схема подключения в Hermes

```yaml
mcp_servers:
  construction-maps:
    command: python
    args: ["-m", "construction_maps_mcp"]
    env:
      YANDEX_MAPS_API_KEY: "${YANDEX_MAPS_API_KEY}"
    enabled: true
```

На практике лучше ставить репозиторий в отдельный venv/uv-окружение и запускать через абсолютный путь к python этого окружения.

## Ограничения и риски

- Росреестр/НСПД используется через неофициальную библиотеку `rosreestr2coord`; API может меняться.
- GitHub API на момент записи показывает `license: null`, хотя README/pyproject декларируют MIT.
- Репозиторий малозвёздный; перед production нужна проверка install/test и реальных запросов.
- Для части функций нужен работающий Yandex Maps API key и включённые API в кабинете Яндекса.

## Связанные заметки

- [[concepts/mcp|MCP — Model Context Protocol]]
- [[entities/hermes-agent|Hermes Agent]]
- [[entities/hermes|Hermes — инфраструктура]]
- [[entities/hermes-marketplace-tools|Marketplace MCP Server]]
