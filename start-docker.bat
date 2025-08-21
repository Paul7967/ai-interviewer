@echo off
chcp 65001 >nul

echo 🚀 Запуск AI Interviewer в Docker...

REM Проверяем наличие Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не установлен. Пожалуйста, установите Docker.
    pause
    exit /b 1
)

REM Проверяем наличие Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose.
    pause
    exit /b 1
)

REM Проверяем наличие .env файла
if not exist .env (
    echo ⚠️  Файл .env не найден. Создаем из примера...
    if exist env.example (
        copy env.example .env >nul
        echo ✅ Файл .env создан. Пожалуйста, отредактируйте его и добавьте ваш OpenAI API ключ.
        echo 📝 Откройте .env файл и замените 'your-openai-api-key' на ваш реальный ключ.
        pause
        exit /b 1
    ) else (
        echo ❌ Файл env.example не найден.
        pause
        exit /b 1
    )
)

REM Останавливаем существующие контейнеры
echo 🛑 Остановка существующих контейнеров...
docker-compose down

REM Собираем и запускаем контейнеры
echo 🔨 Сборка и запуск контейнеров...
docker-compose up --build -d

REM Ждем немного для запуска сервисов
echo ⏳ Ожидание запуска сервисов...
timeout /t 10 /nobreak >nul

REM Проверяем статус контейнеров
echo 📊 Статус контейнеров:
docker-compose ps

echo.
echo 🎉 AI Interviewer запущен!
echo.
echo 📱 Доступные сервисы:
echo    Frontend: http://localhost:5173
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 🔧 Полезные команды:
echo    Просмотр логов: docker-compose logs -f
echo    Остановка: docker-compose down
echo    Перезапуск: docker-compose restart
echo.
echo 📝 Для инициализации базы данных выполните:
echo    docker-compose exec backend python scripts/init_db.py
echo.
pause
