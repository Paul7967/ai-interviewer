#!/bin/bash

# Скрипт для управления Ollama в Docker

OLLAMA_CONTAINER="ai-interviewer-ollama"
OLLAMA_API="http://localhost:11434"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Функция проверки статуса Ollama
check_ollama_status() {
    if curl -f "$OLLAMA_API/api/tags" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Функция запуска Ollama
start_ollama() {
    print_status "Запуск Ollama контейнера..."
    
    if docker ps -q -f name="$OLLAMA_CONTAINER" | grep -q .; then
        print_warning "Контейнер Ollama уже запущен"
        return 0
    fi
    
    # Запускаем контейнер
    docker-compose up -d ollama
    
    if [ $? -eq 0 ]; then
        print_success "Контейнер Ollama запущен"
        
        # Ждем запуска сервера
        print_status "Ожидание запуска сервера..."
        for i in {1..30}; do
            if check_ollama_status; then
                print_success "Ollama сервер готов к работе"
                return 0
            fi
            sleep 2
        done
        
        print_error "Таймаут запуска Ollama сервера"
        return 1
    else
        print_error "Ошибка запуска контейнера Ollama"
        return 1
    fi
}

# Функция остановки Ollama
stop_ollama() {
    print_status "Остановка Ollama контейнера..."
    docker-compose stop ollama
    print_success "Контейнер Ollama остановлен"
}

# Функция перезапуска Ollama
restart_ollama() {
    print_status "Перезапуск Ollama..."
    stop_ollama
    sleep 2
    start_ollama
}

# Функция показа статуса
show_status() {
    print_status "Статус Ollama контейнера:"
    
    if docker ps -q -f name="$OLLAMA_CONTAINER" | grep -q .; then
        print_success "Контейнер запущен"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep "$OLLAMA_CONTAINER"
        
        if check_ollama_status; then
            print_success "API сервер доступен"
            
            # Показываем информацию о моделях
            print_status "Доступные модели:"
            models_response=$(curl -s "$OLLAMA_API/api/tags")
            if [ $? -eq 0 ] && [ -n "$models_response" ]; then
                echo "$models_response" | grep -o '"name":"[^"]*"' | sed 's/"name":"//g' | sed 's/"//g' | while read model; do
                    echo "  - $model"
                done
            else
                echo "  Нет моделей"
            fi
            
            # Показываем информацию о GPU
            print_status "Информация о GPU:"
            docker exec "$OLLAMA_CONTAINER" nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits 2>/dev/null || echo "  GPU информация недоступна"
        else
            print_warning "API сервер недоступен"
        fi
    else
        print_warning "Контейнер не запущен"
    fi
}

# Функция загрузки модели
pull_model() {
    if [ -z "$1" ]; then
        print_error "Укажите название модели"
        echo "Использование: $0 pull <model_name>"
        return 1
    fi
    
    print_status "Загрузка модели: $1"
    
    if ! check_ollama_status; then
        print_error "Ollama сервер недоступен"
        return 1
    fi
    
    curl -X POST "$OLLAMA_API/api/pull" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$1\"}" \
        --progress-bar
    
    if [ $? -eq 0 ]; then
        print_success "Модель $1 загружена"
    else
        print_error "Ошибка загрузки модели $1"
    fi
}

# Функция запуска модели
run_model() {
    if [ -z "$1" ]; then
        print_error "Укажите название модели"
        echo "Использование: $0 run <model_name> [prompt]"
        return 1
    fi
    
    print_status "Запуск модели: $1"
    
    if ! check_ollama_status; then
        print_error "Ollama сервер недоступен"
        return 1
    fi
    
    if [ -z "$2" ]; then
        # Интерактивный режим
        print_status "Интерактивный режим (Ctrl+C для выхода):"
        response=$(curl -X POST "$OLLAMA_API/api/generate" \
            -H "Content-Type: application/json" \
            -d "{\"model\": \"$1\", \"prompt\": \"Привет! Как дела?\", \"stream\": false}")
        echo "$response" | sed 's/.*"response":"//' | sed 's/".*//' | sed 's/\\n/\n/g' | sed 's/\\"/"/g'
    else
        # Одиночный запрос
        response=$(curl -X POST "$OLLAMA_API/api/generate" \
            -H "Content-Type: application/json" \
            -d "{\"model\": \"$1\", \"prompt\": \"$2\", \"stream\": false}")
        echo "$response" | sed 's/.*"response":"//' | sed 's/".*//' | sed 's/\\n/\n/g' | sed 's/\\"/"/g'
    fi
}

# Функция показа логов
show_logs() {
    print_status "Логи Ollama контейнера:"
    docker logs "$OLLAMA_CONTAINER" -f
}

# Функция показа помощи
show_help() {
    echo "Управление Ollama в Docker"
    echo ""
    echo "Использование: $0 <команда> [параметры]"
    echo ""
    echo "Команды:"
    echo "  start     - Запустить Ollama контейнер"
    echo "  stop      - Остановить Ollama контейнер"
    echo "  restart   - Перезапустить Ollama контейнер"
    echo "  status    - Показать статус Ollama"
    echo "  pull <model> - Загрузить модель"
    echo "  run <model> [prompt] - Запустить модель"
    echo "  logs      - Показать логи контейнера"
    echo "  help      - Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 start"
    echo "  $0 pull codellama:latest"
    echo "  $0 run codellama 'Напиши функцию на Python'"
}

# Основная логика
case "$1" in
    start)
        start_ollama
        ;;
    stop)
        stop_ollama
        ;;
    restart)
        restart_ollama
        ;;
    status)
        show_status
        ;;
    pull)
        pull_model "$2"
        ;;
    run)
        run_model "$2" "$3"
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Неизвестная команда: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
