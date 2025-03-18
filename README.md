# Referral System API

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1+-lightblue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.3+-lightgrey.svg)
![Redis](https://img.shields.io/badge/Redis-7.2+-red.svg)
![Celery](https://img.shields.io/badge/Celery-5.4.0+-green.svg)
![Версия](https://img.shields.io/badge/version-1.0.0-blue)


Referral System API — это RESTful сервис для управления реферальной системой. Проект предоставляет возможность регистрации пользователей, создания и удаления реферальных кодов, а также получения информации о рефералах. Сервис построен с использованием Flask, PostgreSQL и следует принципам чистого кода и ООП.

---

## Функциональные возможности

- **Регистрация и аутентификация**: 
  - Регистрация и вход в систему с использованием JWT-токенов.
  - Сброс и смена пароля.
- **Управление реферальными кодами**: 
  - Создание реферального кода с указанием срока годности.
  - Удаление активного реферального кода (деактивация).
  - Только один активный код на пользователя одновременно.
- **Получение данных**:
  - Поиск реферального кода по email пользователя.
  - Регистрация с использованием реферального кода.
  - Просмотр списка рефералов по ID пользователя.
- **Документация**: Интерактивная документация API через Swagger UI.

### Реализованные опциональные возможности 
- Проверка email через EmailHunter.
- Кеширование реферальных кодов с использованием Redis.
- Отправка сообщений на email через Celery.

---

## Технологический стек

- **Backend**: Flask (Python)
- **База данных**: PostgreSQL + SQLAlchemy (ORM) + Flask-Migrate (миграции) + Redis (кэш, брокер)
- **Очередь задач**: Celery
- **Аутентификация**: Flask-JWT-Extended (JWT-токены)
- **Документация**: Swagger UI
- **Дополнительно**: Werkzeug (хеширование паролей)

---

## Требования

- Python 3.9 или выше
- PostgreSQL 14.3 или выше
- Redis 7.2 или выше
- Celery 5.4.0 или выше
- Docker
- Git (для клонирования репозитория)

---

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/dydyaaa/referal.git
```

### 2. Настройка окружения
Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  
# Для Windows: venv\Scripts\activate
```

### 3. Установка зависимостей
Установите все необходимые пакеты:
```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных
* Запустите файл docker-compose.yaml
```bash
docker compose up --build # При первом запуске
docker compose stop
docker compose start
```
* Создайте файл <span style="color:#e6c07b;">settings.json</span> в корне проекта со следующей структурой:
```json
{
    "SECRET_KEY": "your-secret-key",
    "SQLALCHEMY_DATABASE_URI": "postgresql://user:password@localhost/referral_db",
    "JWT_SECRET_KEY": "your-jwt-secret-key",
    "EMAIL_HUNTER_API_KEY": "api_key",
    "REDIS_URL_CACHE": "redis://localhost:6379/0",
    "REDIS_URL_BROKER": "redis://localhost:6379/1",
    "MAIL_SERVER": "smtp.mail.ru",
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": 0,
    "MAIL_USE_SSL": 1,
    "MAIL_USERNAME": "your_email@mail.ru",
    "MAIL_PASSWORD": "your_password"
}
```

### 5. Инициализация базы данных
Настройте миграции и создайте таблицы
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
-----
### 6. Запуск проекта
```bash
python3 wsgi.py
```
```bash
celery -A app.celery worker --loglevel=info
```
По умолчанию сервер будет доступен по адресу <a href="http://127.0.0.1:5000" style="color:#e6c07b;">http://127.0.0.1:5000</a>
## Установка и запуск через Docker
- 1. Склонируйте репозиторий
- 2. Создайте файл <span style="color:#e6c07b;">settings.json</span>
- 3. Запустите docker compose

## Документация API
```
http://127.0.0.1:5000/swagger
```
## Основные эндпоинты
| Метод   | Эндпоинт                                                    | Описание                     | Аутентификация |
|---------|-------------------------------------------------------------|------------------------------|----------------|
| POST    | <span style="color:#e6c07b;">/auth/register</span>          | Регистрация пользователя     | Нет            |
| POST    | <span style="color:#e6c07b;">/auth/login</span>             | Вход в систему               | Нет            |
| POST    | <span style="color:#e6c07b;">/auth/reset_password</span>    | Сброс пароля                 | Нет            |
| POST    | <span style="color:#e6c07b;">/auth/change_password</span>   | Смена пароля                 | JWT            |
| POST    | <span style="color:#e6c07b;">/referral/code</span>          | Создание реферального кода   | JWT            |
| DELETE  | <span style="color:#e6c07b;">/referral/code</span>          | Удаление активного кода      | JWT            |
| GET     | <span style="color:#e6c07b;">/referral/code/by-email</span> | Получение кода по email      | Нет            |
| GET     | <span style="color:#e6c07b;">/referral/referrals</span>     | Получение списка рефералов   | JWT            |
## Проверка API
API можно проверить по адресу <a href="http://45.143.203.217:5000/swagger" style="color:#e6c07b;">http://45.143.203.217:5000/swagger</a>
## Тестирование
Тесты находятся в папке <span style="color:#e6c07b;">/tests</span>. Для запуска:
```bash
python3 -m unittest
```
Тесты проверяют только status code эндпоинтов
## Структура проекта
```
referral-system-api/
├── app/
│   ├── __init__.py        # Инициализация приложения
│   ├── models/            # Модели базы данных
│   ├── routes/            # Маршруты API
│   ├── services/          # Бизнес-логика
│   ├── utils/             # Утилиты
│   └── static/            # Статические файлы (Swagger JSON)
│   └── tasks/             # Задачи для Celery
├── migrations/            # Миграции базы данных
├── tests/                 # Тесты
├── docker-compose.yaml    # Контейнеры с Postgres, Redis и API
├── logging_config.py      # Конфигурация logger'a
├── settings.json          # Файл с настройками
├── requirements.txt       # Зависимости
└── README.md              # Документация
```



