# AI Interviewer Frontend

React фронтенд для AI Interviewer с TypeScript, Vite и Tailwind CSS.

## 🚀 Запуск серверов

### Запуск только фронтенда
```bash
npm run dev
```

### Запуск только бекенда
```bash
npm run dev:backend
```

### Запуск обоих серверов одновременно (рекомендуется)
```bash
npm run dev:both
```

### Запуск с генерацией типов
```bash
npm run dev:full
```

## 📋 Доступные скрипты

| Команда | Описание |
|---------|----------|
| `npm run dev` | Запуск только фронтенда (Vite) |
| `npm run dev:backend` | Запуск только бекенда (FastAPI) |
| `npm run dev:both` | Запуск обоих серверов через concurrently |
| `npm run dev:full` | Генерация типов + запуск фронтенда |
| `npm run build` | Сборка проекта |
| `npm run preview` | Предварительный просмотр сборки |
| `npm run lint` | Проверка кода ESLint |
| `npm run type-check` | Проверка типов TypeScript |
| `npm run generate-types` | Генерация типов из OpenAPI схемы |

## 🌐 Доступные URL

- **Фронтенд**: http://localhost:5173
- **Бекенд API**: http://localhost:8000
- **API Документация**: http://localhost:8000/docs

## 🔧 Установка зависимостей

```bash
npm install
```

## 🎨 Особенности concurrently

При использовании `npm run dev:both`:

- 🐍 **BACKEND** - логи бекенда (синий цвет)
- ⚛️ **FRONTEND** - логи фронтенда (зеленый цвет)
- Оба сервера запускаются одновременно
- Ctrl+C останавливает оба сервера
- Логи отображаются в одном терминале с цветовым кодированием

## 🐛 Устранение неполадок

### Ошибка "concurrently не найден"
```bash
npm install
```

### CORS ошибки
Убедитесь что бекенд запущен на порту 8000 и фронтенд на порту 5173.

### Проблемы с типами
```bash
npm run generate-types
npm run type-check
```
