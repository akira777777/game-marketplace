#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Тестирование Game Marketplace${NC}"
echo "=================================="

# Функция для тестирования endpoint'а
test_endpoint() {
    local url="$1"
    local expected_status="$2"
    local description="$3"
    
    echo -e "\n${YELLOW}🔍 Тестирую: ${description}${NC}"
    echo "URL: $url"
    
    # Выполняем запрос
    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)
    
    # Проверяем статус код
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✅ Статус: $status_code (ожидался $expected_status)${NC}"
        
        # Показываем первые несколько строк ответа
        if [ ! -z "$body" ]; then
            echo -e "${BLUE}📄 Ответ:${NC}"
            echo "$body" | head -3
            if [ $(echo "$body" | wc -l) -gt 3 ]; then
                echo "..."
            fi
        fi
    else
        echo -e "${RED}❌ Статус: $status_code (ожидался $expected_status)${NC}"
        echo -e "${RED}Ошибка: $body${NC}"
    fi
}

# Проверяем что backend работает
echo -e "${BLUE}🔧 Проверка backend сервера...${NC}"
if ! curl -s "http://localhost:8001/health" > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Backend сервер недоступен на порту 8001${NC}"
    echo -e "${YELLOW}Запускаю backend сервер...${NC}"
    
    cd /mnt/games/Projects/python-dev-env
    ./start_server.sh &
    BACKEND_PID=$!
    
    # Ждём запуска сервера
    sleep 5
    
    if ! curl -s "http://localhost:8001/" > /dev/null 2>&1; then
        echo -e "${RED}❌ Не удалось запустить backend сервер${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Backend сервер запущен${NC}"
fi

# Тесты API endpoints
echo -e "\n${BLUE}🌐 Тестирование API endpoints...${NC}"

# Основная страница
test_endpoint "http://localhost:8001/" 200 "Корневой endpoint"

# Документация API
test_endpoint "http://localhost:8001/docs" 200 "Swagger документация"

# Health check
test_endpoint "http://localhost:8001/health" 404 "Health check (может не существовать)"

# API endpoints
test_endpoint "http://localhost:8001/api/games" 200 "Список игр"
test_endpoint "http://localhost:8001/api/lots" 200 "Список лотов"
test_endpoint "http://localhost:8001/api/users" 404 "Список пользователей (защищенный endpoint)"

echo -e "\n${BLUE}🌐 Проверка production build...${NC}"

# Проверяем production build
if curl -s "http://localhost:4000" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Production build доступен на порту 4000${NC}"
    
    # Тестируем SPA маршруты
    test_endpoint "http://localhost:4000" 200 "Главная страница (production)"
    test_endpoint "http://localhost:4000/catalog" 200 "Страница каталога (должен использовать _redirects)"
    test_endpoint "http://localhost:4000/login" 200 "Страница входа (должен использовать _redirects)"
else
    echo -e "${YELLOW}⚠️  Production build недоступен на порту 4000${NC}"
    echo -e "${YELLOW}Запускаю production build...${NC}"
    
    cd /mnt/games/Projects/python-dev-env/GameMarketplace/frontend
    npx serve dist -p 4000 &
    
    sleep 3
    
    if curl -s "http://localhost:4000" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Production build запущен${NC}"
    else
        echo -e "${RED}❌ Не удалось запустить production build${NC}"
    fi
fi

# Проверка размера и производительности
echo -e "\n${BLUE}📊 Анализ production build...${NC}"

cd /mnt/games/Projects/python-dev-env/GameMarketplace/frontend/dist

echo -e "${YELLOW}📁 Размеры файлов:${NC}"
ls -lh assets/ | head -5

echo -e "\n${YELLOW}📈 Общий размер:${NC}"
total_size=$(du -sh . | cut -f1)
echo "Общий размер dist: $total_size"

# Проверка gzip сжатия
echo -e "\n${YELLOW}🗜️  Проверка сжатия:${NC}"
for file in assets/*.js assets/*.css; do
    if [ -f "$file" ]; then
        original=$(stat -c%s "$file")
        compressed=$(gzip -c "$file" | wc -c)
        ratio=$(( (original - compressed) * 100 / original ))
        filename=$(basename "$file")
        echo "$filename: $original bytes → $compressed bytes (экономия $ratio%)"
        break  # Показываем только первый файл для примера
    fi
done

echo -e "\n${GREEN}🎉 Тестирование завершено!${NC}"
echo -e "${BLUE}📋 Следующие шаги:${NC}"
echo "1. Проверьте что все тесты прошли успешно"
echo "2. Откройте http://localhost:4000 для просмотра production build"
echo "3. Откройте http://localhost:8001/docs для тестирования API"
echo "4. Готово к деплою на Netlify!"