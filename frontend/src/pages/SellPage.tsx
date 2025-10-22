import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const SellPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Продать товар
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
              Создание нового лота
            </h2>
            
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                Форма создания лота будет здесь
              </h3>
              <p className="text-gray-600 dark:text-gray-300 mb-6">
                Здесь будет форма для создания нового лота с полями для названия, описания, цены и другой информации
              </p>
              <Button variant="primary">
                Создать лот
              </Button>
            </div>
          </Card>
        </div>

        <div>
          <Card className="p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Советы для продавцов
            </h3>
            
            <div className="space-y-3 text-sm text-gray-600 dark:text-gray-300">
              <div className="flex items-start">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <div>Используйте понятные и точные названия для ваших лотов</div>
              </div>
              
              <div className="flex items-start">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <div>Добавьте подробное описание товара или услуги</div>
              </div>
              
              <div className="flex items-start">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <div>Установите справедливую цену для быстрой продажи</div>
              </div>
              
              <div className="flex items-start">
                <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <div>Отвечайте быстро на вопросы покупателей</div>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Комиссия платформы
            </h3>
            
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">За сделку:</span>
                <span className="font-medium text-gray-900 dark:text-white">5%</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Минимум:</span>
                <span className="font-medium text-gray-900 dark:text-white">10 ₽</span>
              </div>
              
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-300">Максимум:</span>
                <span className="font-medium text-gray-900 dark:text-white">500 ₽</span>
              </div>
            </div>
            
            <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/50 rounded-lg">
              <p className="text-sm text-blue-700 dark:text-blue-300">
                Комиссия взимается только при успешной продаже
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};