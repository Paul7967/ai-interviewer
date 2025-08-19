import React from 'react';

interface ProgressBarProps {
  current: number;
  total: number;
  score: number;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ current, total, score }) => {
  const progress = (current / total) * 100;
  const averageScore = score / (current - 1) || 0;

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          Прогресс интервью
        </h3>
        <div className="text-right">
          <div className="text-2xl font-bold text-primary-600">
            {current}/{total}
          </div>
          <div className="text-sm text-gray-600">
            вопросов пройдено
          </div>
        </div>
      </div>

      {/* Прогресс-бар */}
      <div className="mb-4">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Прогресс</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-primary-600 h-3 rounded-full transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Статистика */}
      <div className="grid grid-cols-2 gap-4">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-semibold text-gray-900">
            {current - 1}
          </div>
          <div className="text-sm text-gray-600">
            Ответов отправлено
          </div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-semibold text-gray-900">
            {averageScore.toFixed(1)}
          </div>
          <div className="text-sm text-gray-600">
            Средний балл
          </div>
        </div>
      </div>
    </div>
  );
};

