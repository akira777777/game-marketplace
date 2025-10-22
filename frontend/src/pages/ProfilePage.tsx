import React from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/auth';

export const ProfilePage: React.FC = () => {
  const { user, logout } = useAuthStore();

  if (!user) {
    return null;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        Мой профиль
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Основная информация */}
        <div className="lg:col-span-2">
          <Card className="p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Личная информация
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Имя пользователя
                </label>
                <div className="text-gray-900 dark:text-white">
                  {user.username}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Email
                </label>
                <div className="text-gray-900 dark:text-white">
                  {user.email}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Дата регистрации
                </label>
                <div className="text-gray-900 dark:text-white">
                  {new Date(user.created_at).toLocaleDateString('ru-RU')}
                </div>
              </div>
            </div>
            
            <div className="mt-6">
              <Button variant="primary">
                Редактировать профиль
              </Button>
            </div>
          </Card>

          {/* Статистика */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Статистика
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="text-2xl font-bold text-primary-600 dark:text-primary-400 mb-1">
                  0
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  Активных лотов
                </div>
              </div>
              
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="text-2xl font-bold text-green-600 dark:text-green-400 mb-1">
                  0
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  Завершенных сделок
                </div>
              </div>
              
              <div className="text-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-1">
                  0 ₽
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-300">
                  Общая сумма продаж
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Боковая панель */}
        <div>
          <Card className="p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Быстрые действия
            </h3>
            
            <div className="space-y-3">
              <Button variant="primary" className="w-full">
                Создать лот
              </Button>
              
              <Button variant="secondary" className="w-full">
                Мои лоты
              </Button>
              
              <Button variant="secondary" className="w-full">
                История заказов
              </Button>
              
              <Button variant="secondary" className="w-full">
                Настройки
              </Button>
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Безопасность
            </h3>
            
            <div className="space-y-3">
              <Button variant="outline" className="w-full">
                Изменить пароль
              </Button>
              
              <Button variant="outline" className="w-full">
                Настройки приватности
              </Button>
              
              <Button
                variant="outline"
                className="w-full text-red-600 hover:text-red-700 border-red-300 hover:border-red-400"
                onClick={logout}
              >
                Выйти из аккаунта
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};