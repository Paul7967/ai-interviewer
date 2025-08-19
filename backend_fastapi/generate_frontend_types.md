# Генерация типов API для фронтенда

## 📋 Пошаговая инструкция

### ✅ Шаг 1: Экспорт OpenAPI схемы (ВЫПОЛНЕНО)

```bash
python export_openapi.py
```

**Результат**: Создан файл `openapi_schema.json` с полной схемой API

### 🔧 Шаг 2: Установка инструментов генерации

#### **Вариант A: openapi-typescript (рекомендуется)**

```bash
# Установка глобально
npm install -g openapi-typescript

# Или локально в проекте
npm install --save-dev openapi-typescript
```

#### **Вариант B: swagger-typescript-api**

```bash
npm install --save-dev swagger-typescript-api
```

#### **Вариант C: orval (для React Query)**

```bash
npm install --save-dev orval
```

### 🚀 Шаг 3: Генерация типов

#### **Способ 1: openapi-typescript**

```bash
# Из локального файла
npx openapi-typescript openapi_schema.json -o src/types/api.ts

# Или из URL (когда сервер запущен)
npx openapi-typescript http://localhost:8000/openapi.json -o src/types/api.ts
```

#### **Способ 2: swagger-typescript-api**

```bash
npx swagger-typescript-api -p openapi_schema.json -o src/types/api.ts -n apiTypes
```

#### **Способ 3: orval (с React Query)**

Создать файл `orval.config.ts`:
```typescript
import { defineConfig } from 'orval';

export default defineConfig({
  api: {
    input: './openapi_schema.json',
    output: {
      target: './src/types/api.ts',
      client: 'react-query',
      override: {
        mutator: {
          path: './src/lib/api-client.ts',
          name: 'customInstance',
        },
      },
    },
  },
});
```

Затем запустить:
```bash
npx orval
```

### 📁 Шаг 4: Структура фронтенд проекта

```
frontend/
├── src/
│   ├── types/
│   │   └── api.ts              # Сгенерированные типы
│   ├── lib/
│   │   └── api-client.ts       # API клиент
│   ├── hooks/
│   │   └── useInterview.ts     # React Query хуки
│   └── components/
│       └── Interview.tsx       # Компоненты
├── package.json
└── tsconfig.json
```

### 🔧 Шаг 5: Создание API клиента

#### **Файл: src/lib/api-client.ts**

```typescript
import axios from 'axios';

// Базовый URL API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Создание axios инстанса
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерцепторы для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Типизированные методы API
export const interviewAPI = {
  // Начать интервью
  startInterview: async (data: InterviewStartRequest): Promise<InterviewSession> => {
    const response = await apiClient.post('/api/interview/start', data);
    return response.data;
  },

  // Получить вопрос
  getQuestion: async (interviewId: string): Promise<QuestionResponse> => {
    const response = await apiClient.get(`/api/interview/question?interview_id=${interviewId}`);
    return response.data;
  },

  // Отправить ответ
  submitAnswer: async (data: AnswerRequest): Promise<Feedback> => {
    const response = await apiClient.post('/api/interview/answer', data);
    return response.data;
  },

  // Завершить интервью
  endInterview: async (interviewId: string): Promise<InterviewEndResponse> => {
    const response = await apiClient.post(`/api/interview/end?interview_id=${interviewId}`);
    return response.data;
  },
};
```

### 🎣 Шаг 6: Создание React Query хуков

#### **Файл: src/hooks/useInterview.ts**

```typescript
import { useMutation, useQuery } from '@tanstack/react-query';
import { interviewAPI } from '../lib/api-client';
import type { 
  InterviewStartRequest, 
  InterviewSession, 
  AnswerRequest, 
  Feedback,
  QuestionResponse,
  InterviewEndResponse 
} from '../types/api';

// Хук для начала интервью
export const useStartInterview = () => {
  return useMutation({
    mutationFn: (data: InterviewStartRequest) => interviewAPI.startInterview(data),
    onSuccess: (data) => {
      console.log('Интервью начато:', data);
    },
  });
};

// Хук для получения вопроса
export const useGetQuestion = (interviewId: string | null) => {
  return useQuery({
    queryKey: ['question', interviewId],
    queryFn: () => interviewAPI.getQuestion(interviewId!),
    enabled: !!interviewId,
  });
};

// Хук для отправки ответа
export const useSubmitAnswer = () => {
  return useMutation({
    mutationFn: (data: AnswerRequest) => interviewAPI.submitAnswer(data),
    onSuccess: (data) => {
      console.log('Ответ отправлен:', data);
    },
  });
};

// Хук для завершения интервью
export const useEndInterview = () => {
  return useMutation({
    mutationFn: (interviewId: string) => interviewAPI.endInterview(interviewId),
    onSuccess: (data) => {
      console.log('Интервью завершено:', data);
    },
  });
};
```

### 🎯 Шаг 7: Использование в компонентах

#### **Файл: src/components/Interview.tsx**

```typescript
import React, { useState } from 'react';
import { useStartInterview, useGetQuestion, useSubmitAnswer, useEndInterview } from '../hooks/useInterview';
import type { InterviewStartRequest, AnswerRequest } from '../types/api';

export const Interview: React.FC = () => {
  const [interviewId, setInterviewId] = useState<string | null>(null);
  const [answer, setAnswer] = useState('');

  const startInterview = useStartInterview();
  const { data: questionData, refetch: refetchQuestion } = useGetQuestion(interviewId);
  const submitAnswer = useSubmitAnswer();
  const endInterview = useEndInterview();

  const handleStartInterview = async () => {
    const data: InterviewStartRequest = {
      topic: 'javascript-basics',
      difficulty: 'middle',
      question_count: 3,
    };

    try {
      const result = await startInterview.mutateAsync(data);
      setInterviewId(result.id);
    } catch (error) {
      console.error('Ошибка начала интервью:', error);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!interviewId || !questionData?.question) return;

    const data: AnswerRequest = {
      interview_id: interviewId,
      question_id: questionData.question.id,
      answer,
      time_spent: 60,
    };

    try {
      await submitAnswer.mutateAsync(data);
      setAnswer('');
      refetchQuestion();
    } catch (error) {
      console.error('Ошибка отправки ответа:', error);
    }
  };

  const handleEndInterview = async () => {
    if (!interviewId) return;

    try {
      const result = await endInterview.mutateAsync(interviewId);
      console.log('Результат интервью:', result);
      setInterviewId(null);
    } catch (error) {
      console.error('Ошибка завершения интервью:', error);
    }
  };

  return (
    <div>
      <h1>AI Интервьюер</h1>
      
      {!interviewId ? (
        <button onClick={handleStartInterview} disabled={startInterview.isPending}>
          {startInterview.isPending ? 'Начинаем...' : 'Начать интервью'}
        </button>
      ) : (
        <div>
          {questionData?.question && (
            <div>
              <h2>Вопрос {questionData.question.question_number}:</h2>
              <p>{questionData.question.text}</p>
              
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Ваш ответ..."
                rows={4}
              />
              
              <button onClick={handleSubmitAnswer} disabled={submitAnswer.isPending}>
                {submitAnswer.isPending ? 'Отправляем...' : 'Отправить ответ'}
              </button>
            </div>
          )}
          
          <button onClick={handleEndInterview} disabled={endInterview.isPending}>
            {endInterview.isPending ? 'Завершаем...' : 'Завершить интервью'}
          </button>
        </div>
      )}
    </div>
  );
};
```

### 📦 Шаг 8: Установка зависимостей фронтенда

```bash
# Создание React проекта с TypeScript
npx create-react-app frontend --template typescript

# Или для Next.js
npx create-next-app@latest frontend --typescript

# Установка необходимых пакетов
npm install axios @tanstack/react-query
npm install --save-dev openapi-typescript
```

### 🔄 Шаг 9: Автоматизация генерации

#### **Добавить в package.json:**

```json
{
  "scripts": {
    "generate-types": "openapi-typescript openapi_schema.json -o src/types/api.ts",
    "dev": "npm run generate-types && react-scripts start"
  }
}
```

### ✅ Шаг 10: Проверка типов

```bash
# Проверка TypeScript
npx tsc --noEmit

# Запуск проекта
npm start
```

## 🎯 Результат

После выполнения всех шагов у вас будет:

1. ✅ **Типизированный API клиент** с автогенерацией типов
2. ✅ **React Query хуки** для работы с API
3. ✅ **TypeScript поддержка** во всех компонентах
4. ✅ **Автоматическая валидация** типов на этапе компиляции
5. ✅ **IntelliSense** в IDE для всех API вызовов

## 🚀 Быстрый старт

```bash
# 1. Экспорт схемы
python export_openapi.py

# 2. Генерация типов
npx openapi-typescript openapi_schema.json -o ../frontend/src/types/api.ts

# 3. Использование в проекте
cd ../frontend
npm start
```

