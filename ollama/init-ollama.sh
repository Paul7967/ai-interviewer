#!/bin/bash

echo "🚀 Запуск Ollama с поддержкой GPU..."

# Проверяем доступность GPU
echo "🔍 Проверка GPU..."
nvidia-smi > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ GPU обнаружен:"
    nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader,nounits
else
    echo "⚠️  GPU не обнаружен, будет использоваться CPU"
fi

# Проверяем CUDA
echo "🔍 Проверка CUDA..."
nvcc --version > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ CUDA доступен"
else
    echo "⚠️  CUDA не установлен"
fi

# Создаем директорию для моделей если её нет
mkdir -p /root/.ollama/models

# Запускаем Ollama в фоновом режиме
echo "🚀 Запуск Ollama сервера..."
ollama serve &

# Ждем запуска сервера
echo "⏳ Ожидание запуска сервера..."
sleep 10

# Проверяем статус сервера
echo "🔍 Проверка статуса сервера..."
curl -f http://localhost:11434/api/tags > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Ollama сервер запущен успешно"
else
    echo "❌ Ошибка запуска Ollama сервера"
    exit 1
fi

# Показываем доступные модели
echo "📋 Доступные модели:"
ollama list

# Показываем информацию о GPU
echo "🖥️  Информация о GPU:"
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

echo "🎉 Ollama готова к работе!"
echo "📡 API доступен на http://localhost:11434"

# Держим контейнер запущенным
tail -f /dev/null
