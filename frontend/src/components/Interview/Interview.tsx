import React, { useState } from 'react';
import { useStartInterview, useGetQuestion, useSubmitAnswer, useEndInterview } from '../../shared/hooks/useInterview';
import type { components } from '../../types/api';
import { QuestionCard } from './QuestionCard';
import { FeedbackCard } from './FeedbackCard';
import { ProgressBar } from './ProgressBar';

type InterviewStartRequest = components['schemas']['InterviewStartRequest'];
type AnswerRequest = components['schemas']['AnswerRequest'];

export const Interview: React.FC = () => {
  const [interviewId, setInterviewId] = useState<string | null>(null);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState<any>(null);

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
      setFeedback(null);
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
      const feedbackResult = await submitAnswer.mutateAsync(data);
      setFeedback(feedbackResult);
      setAnswer('');
      
      // Обновляем вопрос после небольшой задержки
      setTimeout(() => {
        refetchQuestion();
        setFeedback(null);
      }, 3000);
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
      setFeedback(null);
    } catch (error) {
      console.error('Ошибка завершения интервью:', error);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {!interviewId ? (
        <div className="card text-center">
          <h2 className="text-2xl font-semibold mb-4">
            Готовы начать интервью?
          </h2>
          <p className="text-gray-600 mb-6">
            Вам будет предложено 3 вопроса по JavaScript разной сложности.
            Отвечайте подробно и не торопитесь.
          </p>
          <button
            onClick={handleStartInterview}
            disabled={startInterview.isPending}
            className="btn-primary text-lg px-8 py-3"
          >
            {startInterview.isPending ? 'Начинаем...' : 'Начать интервью'}
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Прогресс */}
          {questionData?.progress && (
            <ProgressBar 
              current={questionData.progress.current}
              total={questionData.progress.total}
              score={questionData.progress.score}
            />
          )}

          {/* Фидбэк */}
          {feedback && (
            <FeedbackCard feedback={feedback} />
          )}

          {/* Вопрос */}
          {questionData?.question && !feedback && (
            <QuestionCard
              question={questionData.question}
              answer={answer}
              onAnswerChange={setAnswer}
              onSubmit={handleSubmitAnswer}
              isSubmitting={submitAnswer.isPending}
            />
          )}

          {/* Кнопка завершения */}
          <div className="text-center">
            <button
              onClick={handleEndInterview}
              disabled={endInterview.isPending}
              className="btn-secondary"
            >
              {endInterview.isPending ? 'Завершаем...' : 'Завершить интервью'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

