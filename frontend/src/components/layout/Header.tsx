import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Search, Menu, X, ShoppingCart, Heart, Bell } from 'lucide-react';
import { useAuthStore } from '@/store/auth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';

export const Header: React.FC = () => {
  const location = useLocation();
  const { user, isAuthenticated, logout } = useAuthStore();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const navigation = [
    { name: 'Каталог', href: '/catalog' },
    { name: 'Продать', href: '/sell' },
    { name: 'Помощь', href: '/help' },
  ];

  const isActivePath = (path: string) => location.pathname === path;

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      // Redirect to catalog with search query
      window.location.href = `/catalog?search=${encodeURIComponent(searchQuery)}`;
    }
  };

  return (
    <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link 
            to="/" 
            className="flex items-center space-x-2 text-primary-600 font-bold text-xl"
          >
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">GM</span>
            </div>
            <span className="hidden sm:block">GameMarketplace</span>
          </Link>

          {/* Search Bar */}
          <div className="flex-1 max-w-2xl mx-4 hidden md:block">
            <form onSubmit={handleSearch} className="relative">
              <Input
                type="text"
                placeholder="Поиск товаров, игр, продавцов..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pr-10"
              />
              <button
                type="submit"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <Search className="h-5 w-5" />
              </button>
            </form>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`text-sm font-medium transition-colors ${
                  isActivePath(item.href)
                    ? 'text-primary-600'
                    : 'text-gray-700 dark:text-gray-300 hover:text-primary-600'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* User Actions */}
          <div className="flex items-center space-x-2">
            {isAuthenticated ? (
              <>
                {/* Notification */}
                <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                  <Bell className="h-5 w-5" />
                </button>

                {/* Favorites */}
                <Link 
                  to="/favorites"
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <Heart className="h-5 w-5" />
                </Link>

                {/* Orders */}
                <Link 
                  to="/orders"
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <ShoppingCart className="h-5 w-5" />
                </Link>

                {/* User Menu */}
                <div className="relative group">
                  <button className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
                    <div className="w-6 h-6 bg-primary-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-xs font-medium">
                        {user?.display_name?.[0] || user?.username?.[0] || 'U'}
                      </span>
                    </div>
                    <span className="hidden lg:block text-sm font-medium text-gray-700 dark:text-gray-300">
                      {user?.display_name || user?.username}
                    </span>
                  </button>

                  {/* Dropdown Menu */}
                  <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                    <div className="py-1">
                      <Link
                        to="/profile"
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        Профиль
                      </Link>
                      <Link
                        to="/my-lots"
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        Мои товары
                      </Link>
                      <Link
                        to="/settings"
                        className="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        Настройки
                      </Link>
                      <hr className="my-1 border-gray-200 dark:border-gray-600" />
                      <button
                        onClick={logout}
                        className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        Выйти
                      </button>
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to="/login">
                  <Button variant="ghost" size="sm">
                    Войти
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm">
                    Регистрация
                  </Button>
                </Link>
              </div>
            )}

            {/* Mobile menu button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-400 hover:text-gray-600"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Search */}
        <div className="md:hidden pb-4">
          <form onSubmit={handleSearch} className="relative">
            <Input
              type="text"
              placeholder="Поиск..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pr-10"
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400"
            >
              <Search className="h-5 w-5" />
            </button>
          </form>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
          <div className="px-4 py-2 space-y-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`block px-3 py-2 text-base font-medium rounded-md ${
                  isActivePath(item.href)
                    ? 'text-primary-600 bg-primary-50 dark:bg-primary-900/20'
                    : 'text-gray-700 dark:text-gray-300 hover:text-primary-600 hover:bg-gray-50 dark:hover:bg-gray-800'
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      )}
    </header>
  );
};