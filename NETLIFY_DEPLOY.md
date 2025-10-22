# Деплой Game Marketplace на Netlify

## 🚀 Быстрый деплой

### Вариант 1: Drag & Drop
1. Выполните build проекта:
   ```bash
   cd frontend && npm run build
   ```
2. Зайдите в [Netlify](https://netlify.com)
3. Перетащите папку `frontend/dist` в область "Deploy manually"

### Вариант 2: Git интеграция (рекомендуется)
1. Создайте репозиторий на GitHub
2. Загрузите код проекта в репозиторий
3. В Netlify выберите "Import from Git"
4. Подключите репозиторий
5. Настройте build settings:
   - **Build command**: `cd frontend && npm run build`
   - **Publish directory**: `frontend/dist`
   - **Node version**: 18

### Вариант 3: Netlify CLI
1. Установите Netlify CLI:
   ```bash
   npm install -g netlify-cli
   ```
2. Войдите в аккаунт:
   ```bash
   netlify login
   ```
3. Деплой:
   ```bash
   cd frontend && npm run build
   netlify deploy --prod --dir=dist
   ```

## ⚙️ Конфигурация

### Файлы конфигурации:
- `netlify.toml` - основная конфигурация Netlify
- `frontend/public/_redirects` - правила перенаправления для SPA
- `.env.production` - переменные окружения для production

### Переменные окружения в Netlify:
1. В настройках сайта Netlify перейдите в "Environment variables"
2. Добавьте:
   ```
   VITE_API_BASE_URL=https://your-backend-api-url.com/api
   VITE_APP_TITLE=Game Marketplace
   VITE_APP_VERSION=1.0.0
   ```

## 🔧 Backend настройка

### Для полной функциональности нужно развернуть backend:

1. **Heroku** (рекомендуется):
   ```bash
   # В корне проекта
   git add .
   git commit -m "Deploy to Heroku"
   heroku create your-app-name
   git push heroku main
   ```

2. **Railway**:
   - Подключите GitHub репозиторий
   - Railway автоматически определит Python проект

3. **Render**:
   - Создайте Web Service
   - Укажите команду запуска: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

### После деплоя backend:
1. Обновите `VITE_API_BASE_URL` в настройках Netlify
2. Настройте CORS в backend для домена Netlify

## 🌐 Результат

После деплоя у вас будет:
- **Frontend**: `https://your-site-name.netlify.app`
- **Backend**: `https://your-backend-url.herokuapp.com` (или другой провайдер)

## 🔐 Безопасность

Netlify автоматически предоставляет:
- ✅ HTTPS сертификат
- ✅ CDN по всему миру
- ✅ DDoS защита
- ✅ Кэширование статических ресурсов

## 📊 Мониторинг

В Netlify доступны:
- Analytics
- Build logs
- Error tracking
- Performance insights

## 🚨 Устранение проблем

### Часто встречающиеся проблемы:

1. **404 на маршрутах**: Убедитесь, что `_redirects` файл настроен правильно
2. **API ошибки**: Проверьте CORS настройки в backend
3. **Build ошибки**: Проверьте Node.js версию (должна быть 18+)
4. **Env переменные**: Убедитесь, что все переменные настроены в Netlify

### Логи:
```bash
# Просмотр логов деплоя
netlify logs

# Локальная разработка с Netlify
netlify dev
```