# Weather Service

## Запуск для разработки

1. Заполнить conf/.env (пример conf/.env.example)

2. Установить зависимости `uv sync`

3. Запустить миграции `make migrate`

4. Запустить приложение `uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload`

## Запуск в докере

1. Заполнить conf/.env (пример conf/.env.example)

2. Запустить миграции `make migrate`

3. Запуск `docker-compose up --build`

## Запуск тестов

1. `pytest`
