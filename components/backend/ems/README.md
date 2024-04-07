# Локальное развертывание проекта

## 1. Установка зависимостей

Убедитесь, что у вас установлен пакетный менеджер **Rye**.
В директории `/components/backend/ems`, прописать следующие команды:

```bash
rye sync
source .venv/bin/activate
```

## 2. Применение миграций к БД

В директории `/components/backend/ems`, прописать следующую команду:

```bash
python -m ems.composites.alembic_runner upgrade head
```

## 3. Создание миграций (опционально)

В директории `/components/backend/ems`, прописать следующую команду:

```bash
python -m ems.composites.alembic_runner revision --autogenerate -m 'your_name'
```

## 4. Откат миграций (опционально)

В директории `/components/backend/ems`, прописать следующую команду:

```bash
python -m ems.composites.alembic_runner downgrade -[1-N]
```

## 5. Запуск http-сервера (DEV)

В директории `/components/backend/ems`, прописать следующую команду:

```bash
rye run uvicorn --app-dir src ems.composites.http_api:app --reload --port 3000 --host 0.0.0.0
```

# DEPLOYMENT
В зависимости от того, нужна ли вам `dev` сборка или `prod`, установите
переменную окружения `COMPOSE_FILE` в нужное значение (можно и
через `.env`-файл).

В `.env`-файле задайте все нужные настройки, после чего выполните
```bash
docker compose up -d
```

# LINTER & FORMATTER
Вы можете применить рекомендованные настройки линтера и форматировщика. Для линтера выполнить:
```bash
rye run ruff check --fix
```

Для форматировщика:
```bash
rye run ruff format
```
