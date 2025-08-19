### API Endpoints для AI-агента-интервьюера

##### 1. Аутентификация и пользователи
Регистрация и вход:

POST /api/auth/register          # Регистрация нового пользователя
POST /api/auth/login             # Вход в систему
POST /api/auth/logout            # Выход из системы
POST /api/auth/refresh           # Обновление токена
POST /api/auth/forgot-password   # Восстановление пароля
POST /api/auth/reset-password    # Сброс пароля

Профиль пользователя:

GET    /api/users/profile        # Получить профиль пользователя
PUT    /api/users/profile        # Обновить профиль
DELETE /api/users/profile        # Удалить аккаунт
GET    /api/users/progress       # Получить прогресс обучения
GET    /api/users/statistics     # Получить статистику интервью

##### 2. Управление интервью
Сессии интервью:
POST   /api/interview/start      # Начать новое интервью
GET    /api/interview/current    # Получить текущую сессию
POST   /api/interview/end        # Завершить интервью
GET    /api/interview/history    # История интервью пользователя
GET    /api/interview/:id        # Получить конкретное интервью
DELETE /api/interview/:id        # Удалить интервью

Вопросы и ответы:
GET    /api/interview/question   # Получить текущий вопрос
POST   /api/interview/answer     # Отправить ответ на вопрос
GET    /api/interview/feedback   # Получить фидбэк на ответ
POST   /api/interview/skip       # Пропустить вопрос

##### 3. База вопросов
Управление вопросами:
GET    /api/questions            # Получить все вопросы (с фильтрами)
GET    /api/questions/:id        # Получить конкретный вопрос
POST   /api/questions            # Создать новый вопрос (админ)
PUT    /api/questions/:id        # Обновить вопрос (админ)
DELETE /api/questions/:id        # Удалить вопрос (админ)

Фильтрация и поиск:
GET    /api/questions/topics     # Получить список тем
GET    /api/questions/difficulty # Получить уровни сложности
GET    /api/questions/search     # Поиск вопросов
GET    /api/questions/random     # Случайный вопрос

##### 4. AI и анализ
Анализ ответов:
POST   /api/ai/analyze-answer    # Анализ ответа AI
POST   /api/ai/generate-question # Генерация вопроса AI
POST   /api/ai/explain-concept   # Объяснение концепции
POST   /api/ai/code-review       # Анализ кода

Персонализация:
GET    /api/ai/recommendations   # Рекомендации по обучению
POST   /api/ai/adapt-difficulty  # Адаптация сложности
GET    /api/ai/learning-path     # Персональный путь обучения

##### 5. Статистика и аналитика
Отчеты:
GET    /api/analytics/overview   # Общая статистика
GET    /api/analytics/topics     # Статистика по темам
GET    /api/analytics/progress   # Прогресс обучения
GET    /api/analytics/weaknesses # Слабые места
GET    /api/analytics/strengths  # Сильные стороны

Экспорт данных:
GET    /api/analytics/export     # Экспорт результатов
GET    /api/analytics/report     # Генерация отчета

6. Системные endpoints
Здоровье системы:
GET    /api/health              # Проверка здоровья сервера
GET    /api/health/ai           # Проверка AI сервисов
GET    /api/health/database     # Проверка базы данных

Конфигурация:
GET    /api/config              # Получить конфигурацию
GET    /api/config/ai-models    # Доступные AI модели

##### 7. WebSocket endpoints (для real-time)
WS /ws/interview               # WebSocket для real-time интервью
WS /ws/chat                    # WebSocket для чата с AI

##### 8. Детальная структура запросов/ответов
Пример POST /api/interview/start:
// Request
{
  "topic": "javascript-basics",
  "difficulty": "middle",
  "questionCount": 10,
  "timeLimit": 30 // минуты
}

// Response
{
  "interviewId": "uuid",
  "session": {
    "id": "uuid",
    "topic": "javascript-basics",
    "difficulty": "middle",
    "currentQuestion": 1,
    "totalQuestions": 10,
    "timeRemaining": 1800,
    "score": 0
  },
  "firstQuestion": {
    "id": "uuid",
    "text": "Объясните разницу между var, let и const",
    "type": "text",
    "timeLimit": 180
  }
}

Пример POST /api/interview/answer:
// Request
{
  "interviewId": "uuid",
  "questionId": "uuid",
  "answer": "var имеет функциональную область видимости...",
  "timeSpent": 120
}

// Response
{
  "feedback": {
    "score": 8,
    "comment": "Отличный ответ! Вы правильно указали...",
    "correctAnswer": "Полный правильный ответ...",
    "suggestions": ["Можно добавить про hoisting", "Упомянуть про temporal dead zone"]
  },
  "nextQuestion": {
    "id": "uuid",
    "text": "Что такое closure в JavaScript?",
    "type": "text",
    "timeLimit": 180
  },
  "progress": {
    "current": 2,
    "total": 10,
    "score": 8
  }
}

##### 9. Приоритеты разработки

#### MVP (первая версия):
POST   /api/interview/start      # Начать новое интервью
POST   /api/interview/end        # Завершить интервью
GET    /api/interview/question   # Получить текущий вопрос
POST   /api/interview/answer     # Отправить ответ на вопрос    
POST   /api/ai/analyze-answer    # Анализ ответа AI
GET    /api/interview/feedback   # Получить фидбэк на ответ
POST   /api/interview/skip       # Пропустить вопрос


#### Вторая итерация:
POST /api/auth/register
POST /api/auth/login
Система профилей и прогресса
Расширенная аналитика
WebSocket для real-time
Адаптивная сложность