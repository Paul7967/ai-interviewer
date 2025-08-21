# AI Interviewer - Docker Setup

Полнофункциональное приложение для проведения технических интервью с использованием AI.

## 🏗️ Архитектура

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   PostgreSQL    │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Database      │
│   :5173         │    │   :8000         │    │   :5432         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Быстрый старт

### Предварительные требования

1. **Docker** и **Docker Compose** установлены
2. **OpenAI API ключ** (для AI функциональности)

### Настройка

1. **Скопируйте переменные окружения:**
   ```bash
   cp .env.example .env
   ```

2. **Отредактируйте .env файл:**
   ```env
   OPENAI_API_KEY=your-openai-api-key
   JWT_SECRET=your-super-secret-jwt-key
   ```

### Запуск

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Остановка всех сервисов
docker-compose down
```

## 📊 Доступные сервисы

После запуска будут доступны:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

## 🔧 Команды управления

### Основные команды
```bash
# Запуск всех сервисов
docker-compose up

# Пересборка и запуск
docker-compose up --build

# Запуск только базы данных
docker-compose up postgres

# Запуск только бэкенда
docker-compose up backend

# Запуск только фронтенда
docker-compose up frontend

# Остановка всех сервисов
docker-compose down

# Просмотр логов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f backend
```

### Работа с базой данных
```bash
# Подключение к базе данных
docker-compose exec postgres psql -U postgres -d ai_interviewer

# Выполнение миграций Prisma
docker-compose exec backend prisma migrate deploy

# Генерация Prisma клиента
docker-compose exec backend prisma generate

# Инициализация начальных данных
docker-compose exec backend python scripts/init_db.py
```

### Разработка
```bash
# Вход в контейнер бэкенда
docker-compose exec backend bash

# Вход в контейнер фронтенда
docker-compose exec frontend sh

# Перезапуск сервиса
docker-compose restart backend
```

## 🗄️ База данных

### Структура
- **users** - пользователи системы
- **questions** - вопросы для интервью
- **interviews** - сессии интервью
- **interview_answers** - ответы пользователей

### Миграции
```bash
# Создание новой миграции
docker-compose exec backend prisma migrate dev --name migration_name

# Применение миграций
docker-compose exec backend prisma migrate deploy

# Сброс базы данных
docker-compose exec backend prisma migrate reset
```

## 🔍 Отладка

### Проблемы с подключением к БД
```bash
# Проверка статуса PostgreSQL
docker-compose exec postgres pg_isready -U postgres

# Проверка логов PostgreSQL
docker-compose logs postgres
```

### Проблемы с Prisma
```bash
# Пересоздание Prisma клиента
docker-compose exec backend prisma generate

# Проверка схемы
docker-compose exec backend prisma validate
```

### Проблемы с сетью
```bash
# Проверка сетей Docker
docker network ls

# Проверка подключения между контейнерами
docker-compose exec backend ping postgres
```

## 📁 Структура проекта

```
ai_interviewier/
├── docker-compose.yml          # Основная конфигурация Docker
├── .env                        # Переменные окружения
├── backend_fastapi/
│   ├── Dockerfile              # Образ бэкенда
│   ├── requirements.txt        # Python зависимости
│   ├── main.py                 # FastAPI приложение
│   └── prisma/
│       └── schema.prisma       # Схема базы данных
├── frontend/
│   ├── Dockerfile              # Образ фронтенда
│   ├── package.json            # Node.js зависимости
│   └── src/                    # React приложение
└── scripts/
    └── init_db.py              # Инициализация БД
```

## 🚀 Продакшен

Для продакшена рекомендуется:

1. **Изменить пароли** в docker-compose.yml
2. **Настроить SSL** через nginx
3. **Использовать внешнюю БД** (например, Supabase)
4. **Настроить мониторинг** и логирование

## 🤝 Разработка

### Добавление новых вопросов
```bash
# Вход в контейнер бэкенда
docker-compose exec backend bash

# Запуск Python shell
python

# Добавление вопроса
from prisma import Prisma
prisma = Prisma()
await prisma.connect()
await prisma.question.create({
    'data': {
        'text': 'Ваш вопрос',
        'category': 'javascript',
        'difficulty': 'medium',
        'correctAnswer': 'Правильный ответ'
    }
})
```

### Обновление зависимостей
```bash
# Обновление Python зависимостей
docker-compose exec backend pip install new-package
docker-compose exec backend pip freeze > requirements.txt

# Обновление Node.js зависимостей
docker-compose exec frontend npm install new-package
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs`
2. Убедитесь, что все порты свободны
3. Проверьте переменные окружения
4. Пересоберите образы: `docker-compose up --build`
