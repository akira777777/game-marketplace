import React from 'react';
import { Link } from 'react-router-dom';
import { Search, TrendingUp, Shield, Zap, Users, Star } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent } from '@/components/ui/Card';

export const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-16 lg:py-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              GameMarketplace
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100">
              Безопасная торговая площадка для игровых товаров и услуг
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/catalog">
                <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                  <Search className="mr-2 h-5 w-5" />
                  Найти товары
                </Button>
              </Link>
              <Link to="/sell">
                <Button size="lg" variant="outline" className="w-full sm:w-auto border-white text-white hover:bg-white hover:text-primary-600">
                  <TrendingUp className="mr-2 h-5 w-5" />
                  Начать продавать
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Почему выбирают нас?
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Современная платформа с передовыми технологиями безопасности
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="text-center">
              <CardContent className="p-6">
                <Shield className="h-12 w-12 mx-auto mb-4 text-primary-600" />
                <h3 className="text-xl font-semibold mb-2">Escrow система</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Гарантия безопасности сделок через систему условного депонирования
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardContent className="p-6">
                <Zap className="h-12 w-12 mx-auto mb-4 text-primary-600" />
                <h3 className="text-xl font-semibold mb-2">Быстрые сделки</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Мгновенная доставка и автоматизированные процессы
                </p>
              </CardContent>
            </Card>

            <Card className="text-center">
              <CardContent className="p-6">
                <Users className="h-12 w-12 mx-auto mb-4 text-primary-600" />
                <h3 className="text-xl font-semibold mb-2">Сообщество</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Большое сообщество игроков и система отзывов
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Popular Games Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Популярные игры
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Найдите товары для ваших любимых игр
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {/* Placeholder для популярных игр */}
            {[1, 2, 3, 4, 5, 6].map((index) => (
              <Card key={index} className="group hover:shadow-lg transition-shadow cursor-pointer">
                <CardContent className="p-4 text-center">
                  <div className="w-16 h-16 mx-auto mb-3 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                    <Star className="h-8 w-8 text-gray-400" />
                  </div>
                  <h4 className="font-medium text-sm">Игра {index}</h4>
                  <p className="text-xs text-gray-500">123 товара</p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center mt-8">
            <Link to="/catalog">
              <Button variant="outline">
                Все игры
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-16 bg-primary-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">1000+</div>
              <div className="text-gray-600 dark:text-gray-300">Активных продавцов</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">5000+</div>
              <div className="text-gray-600 dark:text-gray-300">Товаров</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">10000+</div>
              <div className="text-gray-600 dark:text-gray-300">Завершенных сделок</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary-600 mb-2">4.9</div>
              <div className="text-gray-600 dark:text-gray-300">Средний рейтинг</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Готовы начать?
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
            Присоединяйтесь к тысячам игроков, которые уже торгуют на нашей платформе
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/register">
              <Button size="lg" className="w-full sm:w-auto">
                Регистрация
              </Button>
            </Link>
            <Link to="/login">
              <Button size="lg" variant="outline" className="w-full sm:w-auto">
                Войти
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};