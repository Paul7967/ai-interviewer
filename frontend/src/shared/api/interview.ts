import { apiClient } from './client';
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

// Типизированные методы API для интервью
export const interviewAPI = {
  // Начать интервью
  startInterview: async (data: InterviewStartRequest): Promise<InterviewSession> => {
    const response = await apiClient.post<InterviewSession>('/api/interview/start', data);
    return response.data;
  },

  // Получить вопрос
  getQuestion: async (interviewId: string): Promise<QuestionResponse> => {
    const response = await apiClient.get<QuestionResponse>(`/api/interview/question?interview_id=${interviewId}`);
    return response.data;
  },

  // Отправить ответ
  submitAnswer: async (data: AnswerRequest): Promise<Feedback> => {
    const response = await apiClient.post<Feedback>('/api/interview/answer', data);
    return response.data;
  },

  // Завершить интервью
  endInterview: async (interviewId: string): Promise<InterviewEndResponse> => {
    const response = await apiClient.post<InterviewEndResponse>(`/api/interview/end?interview_id=${interviewId}`);
    return response.data;
  },

  // Получить информацию об API
  getApiInfo: async () => {
    const response = await apiClient.get('/');
    return response.data;
  },
};

