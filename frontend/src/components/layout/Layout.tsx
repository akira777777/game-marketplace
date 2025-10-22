import React from 'react';
import { Header } from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <main className="flex-1">
        {children}
      </main>
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                GameMarketplace
              </h3>
              <p className="text-gray-600 dark:text-gray-300 text-sm">
                Безопасная торговая площадка для игровых товаров и услуг
              </p>
            </div>
            
            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">
                Для покупателей
              </h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="/catalog" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    Каталог
                  </a>
                </li>
                <li>
                  <a href="/help" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    Помощь
                  </a>
                </li>
                <li>
                  <a href="/guarantees" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    Гарантии
                  </a>
                </li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">
                Для продавцов
              </h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="/sell" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    Начать продавать
                  </a>
                </li>
                <li>
                  <a href="/seller-guide" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    Руководство продавца
                  </a>
                </li>
                <li>
                  <a href="/commission" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    Комиссии
                  </a>
                </li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-4">
                Компания
              </h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <a href="/about" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    О нас
                  </a>
                </li>
                <li>
                  <a href="/terms" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    Условия
                  </a>
                </li>
                <li>
                  <a href="/privacy" className="text-gray-600 dark:text-gray-300 hover:text-primary-600">
                    Конфиденциальность
                  </a>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
            <p className="text-center text-sm text-gray-500 dark:text-gray-400">
              © 2025 GameMarketplace. Все права защищены.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};