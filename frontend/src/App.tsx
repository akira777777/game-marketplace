import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Layout } from './components/layout/Layout';
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { CatalogPage } from './pages/CatalogPage';
import { GamePage } from './pages/GamePage';
import { LotPage } from './pages/LotPage';
import { ProfilePage } from './pages/ProfilePage';
import { OrdersPage } from './pages/OrdersPage';
import { SellPage } from './pages/SellPage';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import './styles/globals.css';

// Создаем клиент React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 минут
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Layout>
          <Routes>
            {/* Публичные маршруты */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/catalog" element={<CatalogPage />} />
            <Route path="/game/:gameId" element={<GamePage />} />
            <Route path="/lot/:lotId" element={<LotPage />} />
            
            {/* Защищенные маршруты */}
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/orders"
              element={
                <ProtectedRoute>
                  <OrdersPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/sell"
              element={
                <ProtectedRoute>
                  <SellPage />
                </ProtectedRoute>
              }
            />
            
            {/* 404 страница */}
            <Route 
              path="*" 
              element={
                <div className="min-h-screen flex items-center justify-center">
                  <div className="text-center">
                    <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                      404
                    </h1>
                    <p className="text-gray-600 dark:text-gray-300 mb-8">
                      Страница не найдена
                    </p>
                    <a
                      href="/"
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                      На главную
                    </a>
                  </div>
                </div>
              } 
            />
          </Routes>
        </Layout>
      </Router>
      
      {/* React Query DevTools только в development */}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  );
}

export default App;