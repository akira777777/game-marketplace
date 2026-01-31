import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Card } from '../../components/ui/Card';
import { useAuthStore } from '../../store/auth';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { register } = useAuthStore();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Пароли не совпадают');
      return;
    }

    if (formData.password.length < 6) {
      setError('Пароль должен содержать минимум 6 символов');
      return;
    }

    setIsLoading(true);

    try {
      await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });
      navigate('/');
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      setError(error.response?.data?.detail || 'Ошибка регистрации');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
            Создание аккаунта
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
            Или{' '}
            <Link
              to="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              войдите в существующий аккаунт
            </Link>
          </p>
        </div>

        <Card className="p-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 px-4 py-3 rounded-md text-sm">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="username" className="sr-only">
                Имя пользователя
              </label>
              <Input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                required
                placeholder="Имя пользователя"
                value={formData.username}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="email" className="sr-only">
                Email
              </label>
              <Input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                placeholder="Email адрес"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="password" className="sr-only">
                Пароль
              </label>
              <Input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                placeholder="Пароль (минимум 6 символов)"
                value={formData.password}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="confirmPassword" className="sr-only">
                Подтверждение пароля
              </label>
              <Input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                autoComplete="new-password"
                required
                placeholder="Подтвердите пароль"
                value={formData.confirmPassword}
                onChange={handleChange}
              />
            </div>

            <div className="text-sm text-gray-600 dark:text-gray-400">
              <p>
                Создавая аккаунт, вы соглашаетесь с{' '}
                <a href="/terms" className="text-primary-600 hover:text-primary-500">
                  условиями использования
                </a>{' '}
                и{' '}
                <a href="/privacy" className="text-primary-600 hover:text-primary-500">
                  политикой конфиденциальности
                </a>
              </p>
            </div>

            <div>
              <Button
                type="submit"
                variant="primary"
                size="lg"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Создание аккаунта...' : 'Создать аккаунт'}
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};