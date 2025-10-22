import React from 'react';
import { Button } from '../components/ui/Button';

export const OrdersPage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Мои заказы
      </h1>

      <div className="mb-6">
        <div className="flex flex-wrap gap-2">
          <Button variant="primary" size="sm">
            Все
          </Button>
          <Button variant="outline" size="sm">
            Активные
          </Button>
          <Button variant="outline" size="sm">
            Завершенные
          </Button>
          <Button variant="outline" size="sm">
            Отмененные
          </Button>
        </div>
      </div>

      {/* Пустое состояние */}
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
          У вас пока нет заказов
        </h3>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Найдите интересные лоты в каталоге и сделайте свой первый заказ
        </p>
        <Button variant="primary">
          Перейти в каталог
        </Button>
      </div>
    </div>
  );
};