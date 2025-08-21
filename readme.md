User Balance Service
REST-сервис для управления пользователями и денежными переводами, построенный на FastAPI.

Возможности:
- Создание пользователей с балансом
- Просмотр списка всех пользователей
- Переводы между пользователями
- Валидация email и баланса
- Автоматическая документация API

Установка:

Клонируйте репозиторий:
    git clone https://github.com/pylonee/user_service_fastapi
    cd user-service

Создайте виртуальное окружение:
    python -m venv .venv

Активируйте виртуальное окружение:
    Windows:
    .venv\Scripts\activate

    macOS/Linux:
    source .venv/bin/activate

Установите зависимости:
    pip install -r requirements.txt

Запуск сервера:
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

Сервер будет доступен по адресу: http://localhost:8000

Документация API:
После запуска сервера доступна автоматическая документация:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

API Endpoints:
1. Создание пользователя
POST /users

json
{
  "name": "user name",
  "email": "user@example.com",
  "balance": 0
}

2. Получение списка пользователей
GET /users

3. Перевод
POST /transfer

json
{
  "from_user_id": "uuid-отправителя",
  "to_user_id": "uuid-получателя", 
  "amount": 500.00
}

Валидация и проверки:
- Уникальность email
- Неотрицательный баланс
- Достаточность средств для перевода
- Запрет перевода самому себе
- Валидный формат email
- Положительная сумма перевода

Структура проекта:
user-service/
- main.py          # Основное приложение FastAPI 
- models.py        # Модели
- storage.py       # Хранилище данных в памяти
- requirements.txt # Зависимости
- README.md        # Документация

Примеры использования:

1. Создание пользователя:
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "balance": 1000}'

2. Получение пользователей:
curl "http://localhost:8000/users"

3. Перевод средств:
curl -X POST "http://localhost:8000/transfer" \
  -H "Content-Type: application/json" \
  -d '{"from_user_id": "c6e5a7d0-1234-5678-9abc-def012345678", 
       "to_user_id": "f4e8b2c1-9876-5432-10ab-cdef01234567", 
       "amount": 200}'

Технологии:
FastAPI - веб-фреймворк
Pydantic - валидация данных
UVicorn - ASGI-сервер
Python 3.13 - язык программирования

Особенности реализации:
- Данные хранятся в памяти (не требует БД)
- Использует UUID для идентификации пользователей
- Decimal для точных денежных расчетов
- Полная обработка ошибок с HTTP кодами
- Автоматическая генерация документации


Лицензия:
Это тестовый проект. Исходный код предоставляется только для ознакомления.
Любое использование, копирование или распространение запрещено без разрешения автора.

© 2025 Все права защищены.