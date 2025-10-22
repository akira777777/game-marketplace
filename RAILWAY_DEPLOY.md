# 🚀 Развертывание Backend на Railway

## Подготовка завершена ✅

### Созданные файлы:
- ✅ `railway.toml` - конфигурация Railway
- ✅ `requirements.txt` - зависимости Python
- ✅ `.env.production` - переменные окружения
- ✅ `.gitignore` - исключения git
- ✅ GitHub репозиторий: https://github.com/akira777777/game-marketplace

## Инструкция по развертыванию:

### 1. 🔗 Подключение к Railway

1. Откройте https://railway.app
2. Нажмите **"Start a New Project"**
3. Выберите **"Deploy from GitHub repo"**
4. Авторизуйтесь через GitHub
5. Выберите репозиторий: `akira777777/game-marketplace`

### 2. ⚙️ Настройка проекта

В Railway после создания проекта:

1. Нажмите на ваш сервис
2. Перейдите в **Variables** (вкладка переменных)
3. Добавьте переменные окружения:

```
SECRET_KEY=your-super-secret-production-key-min-32-chars
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
DATABASE_URL=sqlite:///./game_marketplace.db
CORS_ORIGINS=["https://cheerful-cocada-c90721.netlify.app"]
```

### 3. 🏗️ Настройка сборки

Railway автоматически определит:
- ✅ Python приложение
- ✅ Команду запуска из `railway.toml`
- ✅ Зависимости из `requirements.txt`

### 4. 🌐 Получение URL

После успешного деплоя:
1. Перейдите в **Settings** → **Domains**
2. Нажмите **"Generate Domain"**
3. Скопируйте URL (например: `https://your-app-name.railway.app`)

## 🔄 Следующий шаг

После получения Railway URL:
1. Обновите переменную `VITE_API_BASE_URL` в Netlify
2. Протестируйте интеграцию

---

**Статус:** 📋 Готов к развертыванию
**GitHub:** https://github.com/akira777777/game-marketplace
**Railway:** https://railway.app (войдите и создайте проект)