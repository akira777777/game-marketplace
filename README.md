# 🎮 GameMarketplace

> **Статус:** ✅ Готов к production  
> **Deployment:** [Vercel](https://vercel.com)
> **Database:** [Neon (PostgreSQL)](https://neon.tech)

Full-stack торговая площадка для игровых товаров с современным стеком технологий.

## 🚀 Deployment

Проект оптимизирован для развертывания на **Vercel** с использованием базы данных **Neon**.

### Настройка Backend (Vercel + Neon)

1. Создайте базу данных на [Neon.tech](https://neon.tech).
2. В настройках Vercel добавьте следующие переменные окружения:
   ```env
   DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/dbname?sslmode=require
   SECRET_KEY=your-secret-key
   ENVIRONMENT=production
   ```

### Настройка Frontend (Vercel)

Frontend автоматически подхватывает настройки из `vercel.json` в корне проекта.

## 🛠 Технологический стек

### Frontend
- ⚛️ **React 18** + TypeScript
- ⚡ **Vite**
- 🎨 **Tailwind CSS**
- 🔄 **Zustand**
- 📦 **Deployment**: Vercel

### Backend  
- 🐍 **FastAPI**
- 🗄️ **SQLAlchemy** (ORM) + PostgreSQL (Neon)
- 🔐 **JWT Authentication**
- 📝 **Pydantic**
- 🚀 **Deployment**: Vercel Serverless Functions

## 📋 Возможности

- ✅ **Регистрация и аутентификация пользователей**
- ✅ **Каталог игр и товаров**
- ✅ **Создание и управление лотами**
- ✅ **Система заказов и платежей**
- ✅ **Профиль пользователя**
- ✅ **Responsive дизайн**
- ✅ **Production-ready**

## 🏗 Локальная разработка

```bash
# Backend
cd backend
pip install -r requirements.txt
# Установите DATABASE_URL в .env (Neon PostgreSQL)
python -m uvicorn app.main:app --reload --port 8001

# Frontend  
cd frontend
npm install
npm run dev
```

## 📁 Структура проекта

```
GameMarketplace/
├── 🎨 frontend/          # React + Vite + TypeScript
├── 🐍 backend/           # FastAPI + SQLAlchemy (PostgreSQL)
├── 🚀 vercel.json        # Vercel конфигурация
└── 🔧 .gitignore         # Git исключения
```

## 🔐 Безопасность

- ✅ **JWT токены**
- ✅ **CORS** настроен для production
- ✅ **PostgreSQL (Neon)** с SSL
- ✅ **Валидация данных** Pydantic

## 🤝 Вклад в проект

```bash
git clone https://github.com/akira777777/game-marketplace.git
cd game-marketplace
```

## 📄 Лицензия

MIT License

---

**🎯 Статус проекта**: Production Ready (Vercel + Neon)
**👨‍💻 Developed**: Full-stack TypeScript/Python архитектура