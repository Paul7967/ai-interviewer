import React from 'react';
import type { Question } from '../../../types/api';

interface QuestionCardProps {
  question: Question;
  answer: string;
  onAnswerChange: (answer: string) => void;
  onSubmit: () => void;
  isSubmitting: boolean;
}

export const QuestionCard: React.FC<QuestionCardProps> = ({
  question,
  answer,
  onAnswerChange,
  onSubmit,
  isSubmitting,
}) => {
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'junior':
        return 'bg-green-100 text-green-800';
      case 'middle':
        return 'bg-yellow-100 text-yellow-800';
      case 'senior':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyText = (difficulty: string) => {
    switch (difficulty) {
      case 'junior':
        return 'Начинающий';
      case 'middle':
        return 'Средний';
      case 'senior':
        return 'Продвинутый';
      default:
        return difficulty;
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">
          Вопрос {question.question_number}
        </h2>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(question.difficulty)}`}>
          {getDifficultyText(question.difficulty)}
        </span>
      </div>

      <div className="mb-6">
        <p className="text-lg text-gray-700 leading-relaxed">
          {question.text}
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <label htmlFor="answer" className="block text-sm font-medium text-gray-700 mb-2">
            Ваш ответ:
          </label>
          <textarea
            id="answer"
            value={answer}
            onChange={(e) => onAnswerChange(e.target.value)}
            placeholder="Опишите ваш ответ подробно..."
            rows={6}
            className="input-field resize-none"
            disabled={isSubmitting}
          />
        </div>

        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-500">
            Минимум 10 символов
          </div>
          <button
            onClick={onSubmit}
            disabled={isSubmitting || answer.trim().length < 10}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Отправляем...' : 'Отправить ответ'}
          </button>
        </div>
      </div>
    </div>
  );
};

