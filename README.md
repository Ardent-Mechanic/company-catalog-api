# Company Catalog API

Локальный каталог организаций с поддержкой PostGIS и асинхронного доступа через FastAPI.

## Быстрый старт

1. Скопируйте переменные окружения: [.env.example](.env.example) → `.env`
```sh
cp .env.example .env
```
2. Запустите контейнеры:
```sh
docker-compose up -d --build
```
(см. [docker-compose.yml](docker-compose.yml) и [docker-compose.override.yml](docker-compose.override.yml))

3. Примените миграции:
```sh
pipenv run alembic -c alembic.ini upgrade head
```
(настройки миграций в [alembic.ini](alembic.ini) и [migrations/env.py](migrations/env.py))

4. API будет доступен на http://localhost:8000/docs (точный запуск в [Dockerfile](Dockerfile) / [app/main.py](app/main.py)).


## Тестирование

🧪 pytest-asyncio  
🐳 Testcontainers + PostGIS  
📍 Geo queries  
🔄 Full CRUD + API  
♻️ Auto cleanup

```bash
pipenv run pytest -v
```

## Требования
- Python 3.12
- Pipenv (используется в Dockerfile и Pipfile) — [Pipfile](Pipfile)
- Postgres + PostGIS (образ в [docker-compose.yml](docker-compose.yml))

## структура проекта
```
app/
├── main.py                        # точка входа FastAPI
├── core/
│   ├── config.py                  # все настройки
│   ├── db/
│   │   └── session.py             # асинхронная сессия БД
│   ├── models/                    # SQLAlchemy модели
│   ├── repositories/              # доступ к данным
│   ├── services/                  # бизнес-логика
│   └── schemas/                   # Pydantic-схемы (вход/выход)
├── api/
│   └── api_v1/
│       └── public/
│           └── organization.py    # публичные роуты
migrations/                        # alembic-миграции
docker-compose.yml
docker-compose.override.yml
Pipfile
```

## Основные эндпоинты (public)
- GET /api/v1/organizations/search — поиск с пагинацией ([handler](app/api/api_v1/public/organization.py))  
- GET /api/v1/organizations/nearby — ближайшие организации по координатам  
- GET /api/v1/organizations/in_square — организации в прямоугольнике  
- GET /api/v1/organizations/activity/{activity_name} — поиск по виду деятельности  
- GET /api/v1/organizations/{org_id} — получить организацию по id

## Миграции
- Скрипты миграций в [migrations/versions](migrations/versions). Примеры: [enable postgis](migrations/versions/2026_02_25_1321-4bd966d063c2_enable_postgis.py), [init db](migrations/versions/2026_02_25_1536-69d463712ba9_init_db.py)

## Локальный запуск без Docker
```sh
pipenv install --dev
cp .env.example .env
pipenv run uvicorn app.main:app --reload
```

## Вклад
- Используйте pre-commit (см. [.pre-commit-config.yaml](.pre-commit-config.yaml)).
- Форматирование: black/isort/flake8 в конфиге.

---
