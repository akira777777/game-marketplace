import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Card } from '../components/ui/Card';
import { gamesService } from '../services/games';
import { Game, GameCategory } from '../types';

export const CatalogPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || '');

  // Получение списка игр
  const { data: games, isLoading: gamesLoading } = useQuery({
    queryKey: ['games', searchQuery, selectedCategory],
    queryFn: () => gamesService.getGames({ 
      search: searchQuery || undefined,
      category: selectedCategory || undefined,
    }),
  });

  // Получение категорий
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => gamesService.getCategories(),
  });

  // Синхронизация с URL
  useEffect(() => {
    const params = new URLSearchParams();
    if (searchQuery) params.set('search', searchQuery);
    if (selectedCategory) params.set('category', selectedCategory);
    setSearchParams(params);
  }, [searchQuery, selectedCategory, setSearchParams]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Поиск будет выполнен автоматически через useQuery
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Каталог игр
        </h1>
        
        {/* Поиск и фильтры */}
        <div className="flex flex-col lg:flex-row gap-4 mb-6">
          <form onSubmit={handleSearch} className="flex-1">
            <div className="flex gap-2">
              <Input
                type="text"
                placeholder="Поиск игр..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1"
              />
              <Button type="submit" variant="primary">
                Найти
              </Button>
            </div>
          </form>
          
          <div className="flex gap-2">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">Все категории</option>
              {categories?.map((category: GameCategory) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
            
            {(searchQuery || selectedCategory) && (
              <Button
                variant="secondary"
                onClick={() => {
                  setSearchQuery('');
                  setSelectedCategory('');
                }}
              >
                Сбросить
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Результаты */}
      {gamesLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[...Array(8)].map((_, i) => (
            <Card key={i} className="p-4">
              <div className="animate-pulse">
                <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded mb-4"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
              </div>
            </Card>
          ))}
        </div>
      ) : games && games.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {games.map((game: Game) => (
            <Card key={game.id} className="p-4 hover:shadow-lg transition-shadow">
              <a href={`/game/${game.id}`} className="block">
                <div className="aspect-video bg-gray-200 dark:bg-gray-700 rounded mb-4 overflow-hidden">
                  {game.image_url ? (
                    <img
                      src={game.image_url}
                      alt={game.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-gray-400">
                      <svg className="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                      </svg>
                    </div>
                  )}
                </div>
                
                <h3 className="font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
                  {game.name}
                </h3>
                
                {game.description && (
                  <p className="text-sm text-gray-600 dark:text-gray-300 line-clamp-3 mb-3">
                    {game.description}
                  </p>
                )}
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {game.category?.name || 'Без категории'}
                  </span>
                  <span className="text-sm font-medium text-primary-600 dark:text-primary-400">
                    Смотреть →
                  </span>
                </div>
              </a>
            </Card>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            Игры не найдены
          </h3>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            Попробуйте изменить параметры поиска
          </p>
          <Button
            variant="primary"
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('');
            }}
          >
            Показать все игры
          </Button>
        </div>
      )}
    </div>
  );
};