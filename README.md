# Referral System API

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.3+-lightgrey.svg)
![Redis](https://img.shields.io/badge/Redis-7.2+-red.svg)

Referral System API — это RESTful сервис для управления реферальной системой. Проект предоставляет возможность регистрации пользователей, создания и удаления реферальных кодов, а также получения информации о рефералах. Сервис построен с использованием Flask, PostgreSQL и следует принципам чистого кода и ООП.

---

## Функциональные возможности

- **Регистрация и аутентификация**: Пользователи могут регистрироваться и входить в систему с использованием JWT-токенов.
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

---

## Технологический стек

- **Backend**: Flask (Python)
- **База данных**: PostgreSQL + SQLAlchemy (ORM) + Flask-Migrate (миграции) + Redis (кэш)
- **Аутентификация**: Flask-JWT-Extended (JWT-токены)
- **Документация**: Swagger UI
- **Дополнительно**: Werkzeug (хеширование паролей)

---

## Требования

- Python 3.9 или выше
- PostgreSQL 14.3 или выше
- Redis 7.2 или выше
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
source venv/bin/activate  # Для Windows: venv\Scripts\activate
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
    "REDIS_URL": "redis://localhost:6379/0"
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
По умолчанию сервер будет доступен по адресу <a href="http://127.0.0.1:5000" style="color:#e6c07b;">http://127.0.0.1:5000</a>
### 7. Документация API
```
http://127.0.0.1:5000/swagger
```
### 8. Основные эндпоинты
| Метод   | Эндпоинт                                                    | Описание                     | Аутентификация |
|---------|-------------------------------------------------------------|------------------------------|----------------|
| POST    | <span style="color:#e6c07b;">/auth/register</span>          | Регистрация пользователя     | Нет            |
| POST    | <span style="color:#e6c07b;">/auth/login</span>             | Вход в систему               | Нет            |
| POST    | <span style="color:#e6c07b;">/referral/code</span>          | Создание реферального кода   | JWT            |
| DELETE  | <span style="color:#e6c07b;">/referral/code</span>          | Удаление активного кода      | JWT            |
| GET     | <span style="color:#e6c07b;">/referral/code/by-email</span> | Получение кода по email      | Нет            |
| GET     | <span style="color:#e6c07b;">/referral/referrals</span>     | Получение списка рефералов   | JWT            |

### 9. Тестирование
Тесты находятся в папке <span style="color:#e6c07b;">/tests</span>. Для запуска:
```bash
python3 -m unittest
```
Тестов пока нет, но когда-нибудь я их деделаю, общеаю.

### 10. Структура проекта
```
referral-system-api/
├── app/
│   ├── __init__.py        # Инициализация приложения
│   ├── models/            # Модели базы данных
│   ├── routes/            # Маршруты API
│   ├── services/          # Бизнес-логика
│   ├── utils/             # Утилиты
│   └── static/            # Статические файлы (Swagger JSON)
├── migrations/            # Миграции базы данных
├── tests/                 # Тесты
├── docker-compose.yaml    # Контейнеры с Postgres и Redis
├── logging_config.py      # Конфигурация logger'a
├── settings.json          # Файл с настройками
├── requirements.txt       # Зависимости
└── README.md              # Документация
```



