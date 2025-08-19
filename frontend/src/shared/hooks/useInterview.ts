import { useMutation, useQuery } from '@tanstack/react-query';
import { interviewAPI } from '../api/interview';
import type { components } from '../../types/api';

type InterviewStartRequest = components['schemas']['InterviewStartRequest'];
type InterviewSession = components['schemas']['InterviewSession'];
type AnswerRequest = components['schemas']['AnswerRequest'];
type Feedback = components['schemas']['Feedback'];

// Временные типы для ответов, которые не определены в схеме
interface QuestionResponse {
  question: {
    id: string;
    text: string;
    topic: string;
    difficulty: string;
    question_number: number;
  };
  progress: {
    current: number;
    total: number;
    score: number;
  };
}

interface InterviewEndResponse {
  message: string;
  final_score: number;
  max_possible_score: number;
  percentage: number;
  questions_answered: number;
  total_questions: number;
}

// Ключи для React Query
export const interviewKeys = {
  all: ['interview'] as const,
  session: (id: string) => [...interviewKeys.all, 'session', id] as const,
  question: (id: string) => [...interviewKeys.all, 'question', id] as const,
  apiInfo: () => [...interviewKeys.all, 'api-info'] as const,
};

// Хук для получения информации об API
export const useApiInfo = () => {
  return useQuery({
    queryKey: interviewKeys.apiInfo(),
    queryFn: interviewAPI.getApiInfo,
    staleTime: 5 * 60 * 1000, // 5 минут
  });
};

// Хук для начала интервью
export const useStartInterview = () => {
  return useMutation({
    mutationFn: (data: InterviewStartRequest) => interviewAPI.startInterview(data),
    onSuccess: (data) => {
      console.log('✅ Интервью начато:', data);
    },
    onError: (error) => {
      console.error('❌ Ошибка начала интервью:', error);
    },
  });
};

// Хук для получения вопроса
export const useGetQuestion = (interviewId: string | null) => {
  return useQuery({
    queryKey: interviewKeys.question(interviewId || ''),
    queryFn: () => interviewAPI.getQuestion(interviewId!),
    enabled: !!interviewId,
    staleTime: 0, // Всегда свежие данные
    retry: 1, // Повторить только 1 раз при ошибке
  });
};

// Хук для отправки ответа
export const useSubmitAnswer = () => {
  return useMutation({
    mutationFn: (data: AnswerRequest) => interviewAPI.submitAnswer(data),
    onSuccess: (data) => {
      console.log('✅ Ответ отправлен:', data);
    },
    onError: (error) => {
      console.error('❌ Ошибка отправки ответа:', error);
    },
  });
};

// Хук для завершения интервью
export const useEndInterview = () => {
  return useMutation({
    mutationFn: (interviewId: string) => interviewAPI.endInterview(interviewId),
    onSuccess: (data) => {
      console.log('✅ Интервью завершено:', data);
    },
    onError: (error) => {
      console.error('❌ Ошибка завершения интервью:', error);
    },
  });
};

