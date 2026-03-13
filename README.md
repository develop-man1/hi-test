# Organisation API

REST API для управления организационной структурой: подразделениями и сотрудниками

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy** (async) — ORM
- **PostgreSQL** — база данных
- **Alembic** — миграции
- **Docker / docker-compose** — контейнеризация

## Структура проекта
```
app/
├── api/v1/          # Роутеры
├── core/            # Конфиг, БД
├── crud/            # Запросы к БД
├── models/          # SQLAlchemy модели
├── schemas/         # Pydantic схемы
├── services/        # Бизнес-логика
alembic/             # Миграции
```

## Запуск

### 1. Клонировать репозиторий
```bash
git clone <ссылка на репозиторий>
cd <папка проекта>
```

### 2. Создать `.env` файл в корне проекта
```bash
cp app/core/.env.example .env
```

Заполнить своими значениями:
```
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/dbname
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=dbname
```

### 3. Запустить
```bash
docker-compose up --build
```

Миграции применятся автоматически. API будет доступен на `http://localhost:8000`.

Документация: `http://localhost:8000/docs`

## Методы API

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/v1/departments/` | Создать подразделение |
| GET | `/api/v1/departments/{id}` | Получить подразделение с деревом |
| PATCH | `/api/v1/departments/{id}` | Обновить подразделение |
| DELETE | `/api/v1/departments/{id}` | Удалить подразделение |
| POST | `/api/v1/departments/{id}/employees/` | Создать сотрудника |

## Бизнес-логика

- Уникальность имени подразделения в пределах одного родителя
- Защита от циклов в дереве (409 Conflict)
- Нельзя сделать подразделение родителем самого себя
- Удаление в режиме `cascade` — удаляет всё поддерево
- Удаление в режиме `reassign` — переводит сотрудников в другой отдел