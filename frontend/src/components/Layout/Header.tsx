import React from 'react';
import { Link, useLocation } from 'react-router';

export const Header: React.FC = () => {
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Логотип и название */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3">
                <h1 className="text-xl font-bold text-gray-900">
                  AI Interviewer
                </h1>
            </Link>
          </div>

          {/* Навигация */}
          <nav className="flex items-center space-x-8">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                isActive('/')
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              Интервью
            </Link>
            
            <Link
              to="/history"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                isActive('/history')
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              История
            </Link>
            
            <Link
              to="/profile"
              className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                isActive('/profile')
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              Профиль
            </Link>
          </nav>

        </div>
      </div>
    </header>
  );
};
