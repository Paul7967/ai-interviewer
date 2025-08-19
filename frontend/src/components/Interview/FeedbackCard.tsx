import React from 'react';
import type { Feedback } from '../../../types/api';

interface FeedbackCardProps {
  feedback: Feedback;
}

export const FeedbackCard: React.FC<FeedbackCardProps> = ({ feedback }) => {
  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-yellow-600';
    if (score >= 4) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreText = (score: number) => {
    if (score >= 8) return 'Отлично!';
    if (score >= 6) return 'Хорошо!';
    if (score >= 4) return 'Удовлетворительно';
    return 'Требует улучшения';
  };

  return (
    <div className="card border-l-4 border-primary-500">
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-xl font-semibold text-gray-900">
          Оценка ответа
        </h3>
        <div className="text-right">
          <div className={`text-2xl font-bold ${getScoreColor(feedback.score)}`}>
            {feedback.score}/10
          </div>
          <div className="text-sm text-gray-600">
            {getScoreText(feedback.score)}
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {/* Комментарий */}
        <div>
          <h4 className="font-medium text-gray-900 mb-2">Комментарий:</h4>
          <p className="text-gray-700 leading-relaxed">
            {feedback.comment}
          </p>
        </div>

        {/* Рекомендации */}
        {feedback.suggestions && feedback.suggestions.length > 0 && (
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Рекомендации для улучшения:</h4>
            <ul className="list-disc list-inside space-y-1 text-gray-700">
              {feedback.suggestions.map((suggestion, index) => (
                <li key={index}>{suggestion}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Правильный ответ */}
        <div>
          <h4 className="font-medium text-gray-900 mb-2">Правильный ответ:</h4>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-gray-700 leading-relaxed">
              {feedback.correct_answer}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

