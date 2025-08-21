# 🐳 Docker Setup - AI Interviewer

## Быстрый старт

### 1. Подготовка
```bash
# Скопируйте переменные окружения
cp env.example .env

# Отредактируйте .env файл и добавьте ваш OpenAI API ключ
# OPENAI_API_KEY=your-real-openai-api-key
```

### 2. Запуск
```bash
# Windows
start-docker.bat

# Linux/Mac
./start-docker.sh

# Или вручную
docker-compose up --build
```

### 3. Инициализация БД
```bash
docker-compose exec backend python scripts/init_db.py
```

## 📊 Доступные сервисы

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

## 🔧 Основные команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Логи
docker-compose logs -f

# Пересборка
docker-compose up --build
```

## 🚨 Устранение проблем

### Проблема: Порт занят
```bash
# Остановите все контейнеры
docker-compose down

# Проверьте, что порты свободны
netstat -an | findstr :5173
netstat -an | findstr :8000
netstat -an | findstr :5432
```

### Проблема: База данных не подключается
```bash
# Проверьте статус PostgreSQL
docker-compose exec postgres pg_isready -U postgres

# Перезапустите только БД
docker-compose restart postgres
```

### Проблема: Prisma ошибки
```bash
# Пересоздайте Prisma клиент
docker-compose exec backend prisma generate

# Примените миграции
docker-compose exec backend prisma migrate deploy
```
