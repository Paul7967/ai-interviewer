# Используем официальный образ Ollama
FROM ollama/ollama:latest

# Устанавливаем дополнительные инструменты для мониторинга
RUN apt-get update && apt-get install -y \
    curl \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Создаем директорию для моделей
RUN mkdir -p /root/.ollama/models

# Устанавливаем переменные окружения для GPU
ENV CUDA_VISIBLE_DEVICES=0
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=*

# Открываем порт для API
EXPOSE 11434

# Используем ENTRYPOINT из базового образа
# CMD будет переопределен в docker-compose
