import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';
import { gamesService } from '../services/games';
import { lotsService } from '../services/lots';

export const GamePage: React.FC = () => {
  const { gameId } = useParams<{ gameId: string }>();

  const { data: game, isLoading: gameLoading } = useQuery({
    queryKey: ['game', gameId],
    queryFn: () => gamesService.getGame(Number(gameId)),
    enabled: !!gameId,
  });

  const { data: lots, isLoading: lotsLoading } = useQuery({
    queryKey: ['lots', 'game', gameId],
    queryFn: () => lotsService.getLots({ game_id: Number(gameId) }),
    enabled: !!gameId,
  });

  if (gameLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-6"></div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="h-96 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="space-y-4">
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!game) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center py-12">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Игра не найдена
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mb-8">
            Запрашиваемая игра не существует или была удалена
          </p>
          <Button variant="primary" onClick={() => window.history.back()}>
            Назад
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Хлебные крошки */}
      <nav className="flex mb-8 text-sm">
        <a href="/" className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
          Главная
        </a>
        <span className="mx-2 text-gray-400">/</span>
        <a href="/catalog" className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
          Каталог
        </a>
        <span className="mx-2 text-gray-400">/</span>
        <span className="text-gray-900 dark:text-white">{game.name}</span>
      </nav>

      {/* Информация об игре */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <div>
          <div className="aspect-video bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden">
            {game.image_url ? (
              <img
                src={game.image_url}
                alt={game.name}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                </svg>
              </div>
            )}
          </div>
        </div>

        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            {game.name}
          </h1>

          {game.category && (
            <div className="mb-4">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200">
                {game.category.name}
              </span>
            </div>
          )}

          {game.description && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Описание
              </h3>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                {game.description}
              </p>
            </div>
          )}

          <div className="space-y-4">
            <Button variant="primary" size="lg" className="w-full">
              Создать лот для этой игры
            </Button>
          </div>
        </div>
      </div>

      {/* Активные лоты */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
          Активные лоты
        </h2>

        {lotsLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Card key={i} className="p-6">
                <div className="animate-pulse">
                  <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded mb-2"></div>
                  <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3 mb-4"></div>
                  <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded"></div>
                </div>
              </Card>
            ))}
          </div>
        ) : lots && lots.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {lots.map((lot) => (
              <Card key={lot.id} className="p-6 hover:shadow-lg transition-shadow">
                <a href={`/lot/${lot.id}`} className="block">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                    {lot.title}
                  </h3>
                  
                  <p className="text-sm text-gray-600 dark:text-gray-300 mb-3 line-clamp-2">
                    {lot.description}
                  </p>
                  
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-lg font-bold text-primary-600 dark:text-primary-400">
                      {lot.price} ₽
                    </span>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      lot.status === 'active' 
                        ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                        : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200'
                    }`}>
                      {lot.status === 'active' ? 'Активен' : 'Неактивен'}
                    </span>
                  </div>
                  
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    Продавец: {lot.seller?.username || 'Неизвестный продавец'}
                  </div>
                </a>
              </Card>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <svg className="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Пока нет активных лотов
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Станьте первым, кто создаст лот для этой игры
            </p>
            <Button variant="primary">
              Создать лот
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};