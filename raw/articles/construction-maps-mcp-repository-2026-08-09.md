---
source_url: https://github.com/alexgrebeshok-coder/construction-maps-mcp
ingested: 2026-08-09
sha256: 7590beba8c5e8d8d9f4a5bde0316039c4400777fe7d09021142b59142ee29fff
title: Construction Maps MCP Server — repository snapshot
---

# Construction Maps MCP Server — repository snapshot

**Repository:** https://github.com/alexgrebeshok-coder/construction-maps-mcp
**Description:** MCP сервер для анализа земельных участков в строительстве (Росреестр + Yandex Maps)
**Default branch:** main
**Latest observed main commit:** 3b1b258ddcceaeb090460e739a882d4f7422b330 — 2026-07-05, docs(security): Yandex key rotation prep
**Latest pushed_at observed via GitHub API:** 2026-07-19T05:26:04Z
**Language:** Python
**License:** README/pyproject declare MIT; GitHub API license field is null
**Topics:** construction, geodata, mcp, rosreestr
**Stars/Forks at ingest:** 0 / 0

## README extract — назначение

Construction Maps MCP Server — MCP-сервер для анализа земельных участков в строительстве. Интегрирует данные Росреестра/НСПД и Yandex Maps для предпроектного анализа участков.

## MCP tools from README

### Кадастр
- `cadastre_get_boundaries` — границы участка по кадастровому номеру (GeoJSON)
- `cadastre_get_info` — информация об участке: площадь, адрес, категория
- `cadastre_search_by_address` — поиск участков по адресу

### Геокодирование
- `geocode_address_to_coords` — адрес → координаты
- `geocode_coords_to_address` — координаты → адрес
- `geocode_validate_address` — проверка адреса

### Инфраструктура
- `infrastructure_find_nearby` — поиск объектов в радиусе: школы, больницы, АЗС и т.п.
- `infrastructure_calculate_distances` — расстояния до поставщиков/точек
- `infrastructure_get_satellite_image` — спутниковый снимок участка

### Геометрия
- `geometry_calculate_area` — площадь полигона
- `geometry_check_intersection` — пересечение участков
- `geometry_measure_distance` — расстояние между точками
- `geometry_buffer` — буфер вокруг геометрии

### Визуализация
- `visualization_generate_static_map` — статическая карта с маркерами
- `visualization_export_geojson` — экспорт в GeoJSON
- `export_to_json` — экспорт данных в JSON

## Requirements and dependencies

From README/pyproject:
- Python >= 3.10
- `mcp>=1.0.0`
- `rosreestr2coord>=3.0.0`
- `shapely>=2.0.0`
- `geomet>=1.0.0`
- `aiohttp`, `requests`
- `cachetools`, `aiosqlite`
- `pydantic`, `pydantic-settings`, `python-dotenv`
- `backoff`, `structlog`

## Configuration from README

Required environment variable:

```env
YANDEX_MAPS_API_KEY=your_api_key_here
```

Optional environment variables:

```env
CACHE_DIR=~/.construction_maps_mcp
CACHE_MAX_SIZE_MB=500
YANDEX_RATE_LIMIT_RPM=15
ROSREESTR_RATE_LIMIT_RPM=30
```

## Architecture notes from README

- Two-level cache: in-memory via cachetools and persistent SQLite cache at `~/.construction_maps_mcp/cache.db`.
- TTL strategy:
  - cadastral boundaries: 30 days;
  - geocoding: 7 days;
  - infrastructure: 1 day;
  - satellite images: 90 days.
- Rate limiting:
  - Yandex Maps: 15 requests/minute;
  - Rosreestr/NSPD: 30 requests/minute.

## Example use case from README

Предпроектный анализ участка:

```text
Проанализируй участок 77:07:0001002:1002:
1. Покажи границы и площадь
2. Найди школы и больницы в радиусе 2 км
3. Создай спутниковую карту
4. Экспортируй в GeoJSON
```

Expected tool calls:
- `cadastre_get_boundaries("77:07:0001002:1002")`
- `infrastructure_find_nearby(lon, lat, 2000, ["school", "hospital"])`
- `infrastructure_get_satellite_image(lon, lat, zoom=15)`
- `visualization_export_geojson("77:07:0001002:1002")`

## Hermes integration draft

Potential Hermes MCP config shape, after repository is installed in a stable local path:

```yaml
mcp_servers:
  construction-maps:
    command: python
    args: ["-m", "construction_maps_mcp"]
    env:
      YANDEX_MAPS_API_KEY: "${YANDEX_MAPS_API_KEY}"
    enabled: true
```

Secrets must remain in Hermes environment/config secret storage, not in wiki pages.
