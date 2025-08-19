# AI Interviewer API - FastAPI Backend

✅ **ГОТОВ К ИСПОЛЬЗОВАНИЮ!** Простой FastAPI сервер для проведения технических интервью по JavaScript.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install --user fastapi uvicorn pydantic httpx requests
```

### 2. Запуск сервера

```bash
# Способ 1: Через uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Способ 2: Через Python
python main.py
```

### 3. Тестирование без запуска сервера

```bash
python demo.py
```

### 4. Доступ к API

- **API документация (Swagger UI)**: http://localhost:8000/docs
- **Альтернативная документация (ReDoc)**: http://localhost:8000/redoc
- **Корневой endpoint**: http://localhost:8000/

## 📋 API Endpoints

### 1. Начать интервью
```
POST /api/interview/start
```

**Тело запроса:**
```json
{
  "topic": "javascript-basics",
  "difficulty": "middle",
  "question_count": 10
}
```

**Ответ:**
```json
{
  "id": "64ec6a53-b4e9-4276-9c09-9e1a0a21d550",
  "topic": "javascript-basics",
  "difficulty": "middle",
  "current_question": 1,
  "total_questions": 3,
  "score": 0,
  "start_time": "2025-08-20T00:22:57.989612",
  "is_active": true
}
```

### 2. Получить вопрос
```
GET /api/interview/question?interview_id=uuid
```

**Ответ:**
```json
{
  "question": {
    "id": "q1",
    "text": "Объясните разницу между var, let и const в JavaScript",
    "topic": "javascript-basics",
    "difficulty": "middle",
    "question_number": 1
  },
  "progress": {
    "current": 1,
    "total": 3,
    "score": 0
  }
}
```

### 3. Отправить ответ
```
POST /api/interview/answer
```

**Тело запроса:**
```json
{
  "interview_id": "uuid",
  "question_id": "q1",
  "answer": "var имеет функциональную область видимости...",
  "time_spent": 120
}
```

**Ответ:**
```json
{
  "score": 9,
  "comment": "Отличный ответ! Вы хорошо понимаете концепцию.",
  "suggestions": [
    "Можете добавить практические примеры",
    "Рассмотрите edge cases"
  ],
  "correct_answer": "var имеет функциональную область видимости и поднимается (hoisting), let и const имеют блочную область видимости, const нельзя переназначить"
}
```

### 4. Завершить интервью
```
POST /api/interview/end?interview_id=uuid
```

**Ответ:**
```json
{
  "message": "Интервью завершено",
  "final_score": 18,
  "max_possible_score": 30,
  "percentage": 60.0,
  "questions_answered": 2,
  "total_questions": 3
}
```

## 🧪 Тестирование

### Автоматическое тестирование
```bash
python demo.py
```

**Результат тестирования:**
- ✅ Все 4 endpoints работают корректно
- ✅ Валидация данных работает
- ✅ Анализ ответов функционирует
- ✅ Система подсчета очков работает
- ✅ Прогресс интервью отслеживается

### Ручное тестирование с curl

```bash
# 1. Начать интервью
curl -X POST "http://localhost:8000/api/interview/start" \
     -H "Content-Type: application/json" \
     -d '{
       "topic": "javascript-basics",
       "difficulty": "middle",
       "question_count": 3
     }'

# 2. Получить вопрос (замените YOUR_INTERVIEW_ID)
curl "http://localhost:8000/api/interview/question?interview_id=YOUR_INTERVIEW_ID"

# 3. Отправить ответ
curl -X POST "http://localhost:8000/api/interview/answer" \
     -H "Content-Type: application/json" \
     -d '{
       "interview_id": "YOUR_INTERVIEW_ID",
       "question_id": "q1",
       "answer": "var имеет функциональную область видимости, let и const имеют блочную область видимости",
       "time_spent": 60
     }'

# 4. Завершить интервью
curl -X POST "http://localhost:8000/api/interview/end?interview_id=YOUR_INTERVIEW_ID"
```

## 📊 База вопросов

### Доступные темы:
- **javascript-basics** - Основы JavaScript

### Вопросы в базе:
1. **Объясните разницу между var, let и const в JavaScript** (middle)
2. **Что такое closure в JavaScript?** (middle)
3. **Объясните, что такое Event Loop в JavaScript** (senior)

## 🏗️ Структура проекта

```
backend_fastapi/
├── main.py              # Основной файл приложения
├── demo.py              # Демонстрация работы API
├── test_api.py          # Тестирование с реальным сервером
├── requirements.txt     # Зависимости Python
└── README.md           # Документация
```

## ⚙️ Особенности

- **Хранение в памяти**: Данные хранятся в памяти (перезагружаются при перезапуске)
- **Простой анализ**: Базовая логика анализа ответов (заглушка для AI)
- **Автоматическая документация**: Swagger UI доступен по адресу `/docs`
- **Валидация данных**: Автоматическая валидация с помощью Pydantic
- **Тестирование**: Встроенные тесты без запуска сервера

## 🔮 Следующие шаги

1. **Интеграция с AI**: Добавление Ollama для анализа ответов
2. **База данных**: Переход на PostgreSQL для постоянного хранения
3. **Аутентификация**: Система пользователей и сессий
4. **Расширение вопросов**: Больше тем и вопросов
5. **Адаптивность**: Динамическая сложность вопросов

## 🎯 Результаты тестирования

```
✅ Корневой endpoint: 200 OK
✅ Начало интервью: 200 OK
✅ Получение вопроса: 200 OK
✅ Отправка ответа: 200 OK (оценка: 9/10)
✅ Завершение интервью: 200 OK (итоговая оценка: 60%)
```

**Статус проекта**: 🟢 Готов к использованию!
