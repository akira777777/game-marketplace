# 🎮 GameMarketplace - Gaming Trading Platform

Современная торговая платформа для игровых товаров, вдохновленная FunPay, но с улучшенным UX/UI и современными технологиями.

## 🚀 Особенности

- **🎯 Каталог игр**: Структурированный каталог с популярными играми
- **💰 Торговая площадка**: Безопасная торговля игровыми ценностями
- **🔒 Escrow система**: Гарантия безопасности сделок
- **💬 Встроенный чат**: Мгновенные сообщения между пользователями
- **⭐ Система отзывов**: Рейтинги и отзывы о продавцах
- **🔍 Умный поиск**: Продвинутые фильтры и сортировка
- **📱 Responsive дизайн**: Идеально работает на всех устройствах
- **🌙 Темная тема**: Современный дизайн в темных тонах

## 🛠 Технологии

### Backend
- **FastAPI** - Современный, быстрый веб-фреймворк
- **PostgreSQL** - Надежная реляционная база данных
- **SQLAlchemy** - ORM для работы с БД
- **Redis** - Кэширование и сессии
- **WebSocket** - Реальное время для чата
- **JWT** - Безопасная аутентификация

### Frontend
- **React 18** - Современная библиотека UI
- **TypeScript** - Типизированный JavaScript
- **Vite** - Быстрая сборка
- **TailwindCSS** - Utility-first CSS
- **React Query** - Управление состоянием сервера
- **React Router** - Маршрутизация

## 📁 Структура проекта

```
GameMarketplace/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy модели
│   │   ├── api/           # API эндпоинты
│   │   ├── core/          # Настройки и конфигурация
│   │   ├── services/      # Бизнес логика
│   │   └── utils/         # Вспомогательные функции
│   ├── tests/             # Тесты
│   └── migrations/        # Миграции БД
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React компоненты
│   │   ├── pages/         # Страницы
│   │   ├── hooks/         # Пользовательские хуки
│   │   ├── services/      # API сервисы
│   │   ├── store/         # Управление состоянием
│   │   ├── types/         # TypeScript типы
│   │   └── styles/        # Стили
│   └── public/            # Статические файлы
├── database/              # SQL схемы и скрипты
├── static/                # Медиа файлы
└── docs/                  # Документация
```

## 🚦 Быстрый старт

### 1. Клонирование и настройка

```bash
# Переход в папку проекта
cd /mnt/games/Projects/python-dev-env/GameMarketplace

# Активация виртуальной среды Python
source ../venv/bin/activate

# Установка зависимостей backend
cd backend
pip install -r requirements.txt

# Установка зависимостей frontend  
cd ../frontend
npm install
```

### 2. Настройка базы данных

```bash
# Создание базы данных PostgreSQL
createdb gamemarket

# Запуск миграций
cd backend
alembic upgrade head
```

### 3. Запуск разработки

```bash
# Terminal 1 - Backend API
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend Dev Server  
cd frontend
npm run dev
```

### 4. Открытие в браузере

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 Основные функции

### Для покупателей
- Поиск и фильтрация товаров
- Безопасная покупка через Escrow
- Чат с продавцами
- Отзывы и рейтинги
- История покупок

### Для продавцов
- Создание лотов
- Управление товарами
- Статистика продаж
- Чат с покупателями
- Автоматические уведомления

### Для администраторов
- Модерация лотов
- Управление пользователями
- Аналитика платформы
- Разрешение споров

## 🔒 Безопасность

- Escrow система для защиты сделок
- JWT токены для аутентификации
- Шифрование паролей bcrypt
- Валидация данных Pydantic
- Rate limiting API
- CORS защита

## 📊 API Эндпоинты

### Аутентификация
- `POST /auth/register` - Регистрация
- `POST /auth/login` - Вход
- `POST /auth/refresh` - Обновление токена

### Игры и категории
- `GET /games` - Список игр
- `GET /games/{id}/categories` - Категории игры

### Лоты
- `GET /lots` - Список лотов с фильтрами
- `POST /lots` - Создание лота
- `GET /lots/{id}` - Детали лота

### Заказы
- `POST /orders` - Создание заказа
- `GET /orders/my` - Мои заказы
- `PUT /orders/{id}/status` - Изменение статуса

### Чат
- `WebSocket /ws/chat/{room_id}` - Подключение к чату

## 🧪 Тестирование

```bash
# Backend тесты
cd backend
pytest

# Frontend тесты  
cd frontend
npm run test
```

## 📈 Развертывание

### Docker
```bash
# Сборка и запуск
docker-compose up --build
```

### Production
```bash
# Backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
npm run build
```

## 🤝 Участие в разработке

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🎯 Roadmap

- [ ] Мобильное приложение
- [ ] API для мобильного приложения
- [ ] Интеграция с играми
- [ ] Система партнерства
- [ ] Многоязычность
- [ ] Платежные системы

---

**Создано с ❤️ для геймерского сообщества**