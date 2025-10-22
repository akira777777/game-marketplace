import React from 'react';
import { useParams } from 'react-router-dom';
import { Button } from '../components/ui/Button';

export const LotPage: React.FC = () => {
  const { lotId } = useParams<{ lotId: string }>();

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Страница лота #{lotId}
      </h1>

      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
          Страница лота в разработке
        </h3>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Здесь будет подробная информация о лоте с возможностью покупки
        </p>
        <Button variant="primary" onClick={() => globalThis.history.back()}>
          Назад
        </Button>
      </div>
    </div>
  );
};