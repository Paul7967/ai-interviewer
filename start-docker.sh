#!/bin/bash

# AI Interviewer Docker Startup Script

echo "🚀 Запуск AI Interviewer в Docker..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверяем наличие Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Создаем из примера..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✅ Файл .env создан. Пожалуйста, отредактируйте его и добавьте ваш OpenAI API ключ."
        echo "📝 Откройте .env файл и замените 'your-openai-api-key' на ваш реальный ключ."
        exit 1
    else
        echo "❌ Файл env.example не найден."
        exit 1
    fi
fi

# Останавливаем существующие контейнеры
echo "🛑 Остановка существующих контейнеров..."
docker-compose down

# Собираем и запускаем контейнеры
echo "🔨 Сборка и запуск контейнеров..."
docker-compose up --build -d

# Ждем немного для запуска сервисов
echo "⏳ Ожидание запуска сервисов..."
sleep 10

# Проверяем статус контейнеров
echo "📊 Статус контейнеров:"
docker-compose ps

echo ""
echo "🎉 AI Interviewer запущен!"
echo ""
echo "📱 Доступные сервисы:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔧 Полезные команды:"
echo "   Просмотр логов: docker-compose logs -f"
echo "   Остановка: docker-compose down"
echo "   Перезапуск: docker-compose restart"
echo ""
echo "📝 Для инициализации базы данных выполните:"
echo "   docker-compose exec backend python scripts/init_db.py"
