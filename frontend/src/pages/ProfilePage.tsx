import React from 'react';

export const ProfilePage: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Профиль
        </h1>
        <p className="text-lg text-gray-600">
          Управляйте настройками и просматривайте статистику
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Основная информация */}
        <div className="lg:col-span-2">
          <div className="card mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Основная информация
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Имя
                </label>
                <input
                  type="text"
                  className="input-field"
                  placeholder="Введите ваше имя"
                  defaultValue="Пользователь"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  className="input-field"
                  placeholder="user@example.com"
                  defaultValue="user@example.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Уровень разработчика
                </label>
                <select className="input-field">
                  <option value="junior">Junior</option>
                  <option value="middle" selected>Middle</option>
                  <option value="senior">Senior</option>
                </select>
              </div>
            </div>
          </div>

          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Настройки интервью
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Предпочитаемая сложность
                </label>
                <select className="input-field">
                  <option value="junior">Начинающий</option>
                  <option value="middle" selected>Средний</option>
                  <option value="senior">Продвинутый</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Количество вопросов по умолчанию
                </label>
                <input
                  type="number"
                  className="input-field"
                  min="1"
                  max="20"
                  defaultValue="10"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Статистика */}
        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Статистика
            </h2>
            <div className="space-y-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-primary-600">0</div>
                <div className="text-sm text-gray-600">Интервью пройдено</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-primary-600">0</div>
                <div className="text-sm text-gray-600">Средний балл</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-primary-600">0</div>
                <div className="text-sm text-gray-600">Вопросов отвечено</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
