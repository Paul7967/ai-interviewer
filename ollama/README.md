# Ollama Integration

Интеграция Ollama с поддержкой GPU для проекта AI Interviewer.

## 🚀 Возможности

- ✅ Поддержка GPU (NVIDIA CUDA)
- ✅ API доступ через HTTP
- ✅ Управление моделями
- ✅ Потоковая генерация
- ✅ Мониторинг ресурсов
- ✅ Интеграция с FastAPI backend

## 📋 Требования

- Docker с поддержкой NVIDIA Container Runtime
- NVIDIA GPU с драйверами CUDA
- Docker Compose

## 🛠️ Установка и запуск

### 1. Запуск только Ollama

```bash
# Запуск Ollama с GPU поддержкой
docker-compose -f docker-compose.ollama.yml up -d

# Проверка статуса
./scripts/ollama-manager.sh status
```

### 2. Запуск с основным проектом

```bash
# Запуск всего проекта включая Ollama
docker-compose up -d

# Или только определенные сервисы
docker-compose up -d postgres backend ollama
```

### 3. Управление через скрипт

```bash
# Запуск
./scripts/ollama-manager.sh start

# Остановка
./scripts/ollama-manager.sh stop

# Перезапуск
./scripts/ollama-manager.sh restart

# Статус
./scripts/ollama-manager.sh status

# Логи
./scripts/ollama-manager.sh logs
```

## 📦 Управление моделями

### Загрузка моделей

```bash
# Загрузка Code Llama
./scripts/ollama-manager.sh pull codellama:latest

# Загрузка Stable Code
./scripts/ollama-manager.sh pull stable-code:3b-code-q4_0

# Загрузка Llama 2
./scripts/ollama-manager.sh pull llama2:latest
```

### Использование моделей

```bash
# Запуск модели с промптом
./scripts/ollama-manager.sh run codellama "Напиши функцию на Python для сортировки массива"

# Интерактивный режим
./scripts/ollama-manager.sh run codellama
```

## 🔌 API Endpoints

Ollama API доступен на `http://localhost:11434`

### Основные endpoints:

- `GET /api/tags` - Список моделей
- `POST /api/pull` - Загрузка модели
- `POST /api/generate` - Генерация текста
- `POST /api/chat` - Чат с моделью
- `POST /api/embeddings` - Получение эмбеддингов

### Примеры запросов:

```bash
# Список моделей
curl http://localhost:11434/api/tags

# Генерация текста
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "codellama:latest",
    "prompt": "Напиши функцию на Python",
    "stream": false
  }'

# Загрузка модели
curl -X POST http://localhost:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name": "codellama:latest"}'
```

## 🐍 Python Integration

### Использование в FastAPI

```python
from ollama_client import OllamaClient, OllamaGenerateRequest

# Асинхронное использование
async def generate_code(prompt: str):
    async with OllamaClient() as client:
        request = OllamaGenerateRequest(
            model="codellama:latest",
            prompt=prompt,
            stream=False
        )
        response = await client.generate(request)
        return response.response

# Синхронное использование
from ollama_client import OllamaClientSync

client = OllamaClientSync()
models = client.list_models()
```

### Интеграция с существующим кодом

```python
# В main.py добавьте:
from ollama_client import OllamaClient

@app.get("/ollama/models")
async def get_ollama_models():
    async with OllamaClient() as client:
        if await client.health_check():
            models = await client.list_models()
            return {"models": [model.dict() for model in models]}
        else:
            raise HTTPException(status_code=503, detail="Ollama недоступен")

@app.post("/ollama/generate")
async def generate_with_ollama(prompt: str, model: str = "codellama:latest"):
    async with OllamaClient() as client:
        request = OllamaGenerateRequest(
            model=model,
            prompt=prompt,
            stream=False
        )
        response = await client.generate(request)
        return {"response": response.response}
```

## 🔧 Конфигурация

### Переменные окружения

```bash
# Ollama конфигурация
CUDA_VISIBLE_DEVICES=0          # GPU устройство
OLLAMA_HOST=0.0.0.0            # Хост для API
OLLAMA_ORIGINS=*               # CORS настройки
OLLAMA_DEBUG=INFO              # Уровень логирования
```

### Настройка GPU

```bash
# Проверка GPU
nvidia-smi

# Проверка Docker GPU поддержки
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

## 📊 Мониторинг

### GPU мониторинг

```bash
# Мониторинг GPU в реальном времени
docker exec ai-interviewer-ollama nvidia-smi -l 1

# Информация о памяти
docker exec ai-interviewer-ollama nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

### Логи контейнера

```bash
# Просмотр логов
docker logs ai-interviewer-ollama -f

# Или через скрипт
./scripts/ollama-manager.sh logs
```

## 🚨 Troubleshooting

### Проблемы с GPU

1. **GPU не обнаружен:**
   ```bash
   # Проверьте драйверы
   nvidia-smi
   
   # Проверьте Docker GPU поддержку
   docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
   ```

2. **Недостаточно памяти GPU:**
   ```bash
   # Используйте модели с меньшим размером
   ./scripts/ollama-manager.sh pull stable-code:3b-code-q4_0
   ```

### Проблемы с API

1. **API недоступен:**
   ```bash
   # Проверьте статус контейнера
   docker ps | grep ollama
   
   # Перезапустите контейнер
   ./scripts/ollama-manager.sh restart
   ```

2. **Ошибки подключения:**
   ```bash
   # Проверьте порт
   netstat -tlnp | grep 11434
   
   # Проверьте логи
   ./scripts/ollama-manager.sh logs
   ```

## 📈 Производительность

### Рекомендуемые модели для RTX 4060 (8GB VRAM):

- `codellama:latest` - 3.8GB
- `stable-code:3b-code-q4_0` - 1.6GB
- `llama2:7b-q4_0` - 4GB
- `mistral:7b-q4_0` - 4GB

### Оптимизация:

```bash
# Использование низкоуровневых моделей для экономии памяти
./scripts/ollama-manager.sh pull stable-code:3b-code-q4_0

# Настройка параметров генерации
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "codellama:latest",
    "prompt": "Напиши функцию",
    "options": {
      "num_predict": 100,
      "temperature": 0.7
    }
  }'
```

## 🔗 Полезные ссылки

- [Ollama Documentation](https://ollama.ai/docs)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [NVIDIA Container Runtime](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- [Docker GPU Support](https://docs.docker.com/config/containers/resource_constraints/#gpu)
