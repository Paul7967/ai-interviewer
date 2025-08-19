# AI Interviewer Frontend

Современный React фронтенд для AI-агента-интервьюера по JavaScript.

## 🚀 Технологии

- **Vite** - быстрый сборщик
- **React 18** - UI библиотека
- **TypeScript** - типизация
- **Tailwind CSS** - стилизация
- **React Query** - управление состоянием и кэширование
- **Axios** - HTTP клиент

## 📦 Установка и запуск

### 1. Установка зависимостей

```bash
npm install
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Запуск в режиме разработки

```bash
npm run dev
```

Приложение будет доступно по адресу: http://localhost:5173

### 4. Сборка для продакшена

```bash
npm run build
```

## 🏗️ Структура проекта

```
src/
├── components/           # React компоненты
│   └── Interview/       # Компоненты интервью
│       ├── Interview.tsx
│       ├── QuestionCard.tsx
│       ├── FeedbackCard.tsx
│       └── ProgressBar.tsx
├── pages/               # Страницы приложения
│   └── InterviewPage.tsx
├── shared/              # Общий код
│   ├── api/            # API клиенты
│   │   ├── client.ts
│   │   └── interview.ts
│   └── hooks/          # React Query хуки
│       └── useInterview.ts
├── types/               # TypeScript типы
│   └── api.ts          # Автогенерированные типы API
├── App.tsx             # Главный компонент
└── main.tsx            # Точка входа
```

## 🔧 Основные возможности

### ✅ Типизированный API клиент
- Автогенерация типов из OpenAPI схемы
- Типобезопасные запросы и ответы
- Обработка ошибок

### ✅ React Query интеграция
- Кэширование данных
- Автоматическое обновление
- Оптимистичные обновления
- DevTools для отладки

### ✅ Современный UI
- Responsive дизайн
- Анимации и переходы
- Доступность (a11y)
- Темная/светлая тема (готово к добавлению)

### ✅ Компонентная архитектура
- Переиспользуемые компоненты
- Четкое разделение ответственности
- Легкое тестирование

## 🎯 Функциональность

1. **Начало интервью** - выбор темы и сложности
2. **Отображение вопросов** - с индикатором прогресса
3. **Отправка ответов** - с валидацией
4. **Получение фидбэка** - оценка и рекомендации
5. **Завершение интервью** - итоговая статистика

## 🔄 Автоматическая генерация типов

При изменении API схемы:

```bash
# Обновить схему из backend
copy ..\backend_fastapi\openapi_schema.json .

# Сгенерировать типы
npx openapi-typescript openapi_schema.json -o src/types/api.ts
```

## 🧪 Тестирование

```bash
# Запуск тестов
npm run test

# Проверка типов
npm run type-check
```

## 📱 Адаптивность

Приложение адаптировано для:
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (до 767px)

## 🎨 Кастомизация

### Цветовая схема
Основные цвета определены в `tailwind.config.js`:

```javascript
colors: {
  primary: {
    50: '#eff6ff',
    500: '#3b82f6',
    600: '#2563eb',
    // ...
  }
}
```

### Компоненты
Готовые CSS классы в `src/index.css`:

```css
.btn-primary    /* Основная кнопка */
.btn-secondary  /* Вторичная кнопка */
.input-field    /* Поле ввода */
.card           /* Карточка */
```

## 🚀 Развертывание

### Vercel
```bash
npm run build
# Загрузить папку dist
```

### Netlify
```bash
npm run build
# Загрузить папку dist
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🔧 Разработка

### Добавление нового компонента
1. Создать файл в `src/components/`
2. Добавить типы в `src/types/`
3. Создать хуки в `src/shared/hooks/`
4. Добавить стили в `src/index.css`

### Добавление нового API endpoint
1. Обновить OpenAPI схему
2. Сгенерировать типы
3. Добавить метод в `src/shared/api/`
4. Создать хук в `src/shared/hooks/`

## 📄 Лицензия

MIT
