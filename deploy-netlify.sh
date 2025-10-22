#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Game Marketplace - Деплой на Netlify${NC}"
echo "========================================"

# Проверка наличия директории frontend
if [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Ошибка: Директория frontend не найдена${NC}"
    exit 1
fi

cd frontend

# Проверка наличия node_modules
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Установка зависимостей...${NC}"
    npm install
fi

# Создание production build
echo -e "${BLUE}🔨 Создание production build...${NC}"
npm run build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Build создан успешно!${NC}"
    echo ""
    echo -e "${BLUE}📁 Файлы для деплоя находятся в: ${GREEN}frontend/dist${NC}"
    echo ""
    echo -e "${YELLOW}📋 Следующие шаги:${NC}"
    echo "1. Зайдите на https://netlify.com"
    echo "2. Перетащите папку 'frontend/dist' в зону деплоя"
    echo "3. Или используйте Netlify CLI:"
    echo "   ${BLUE}netlify deploy --prod --dir=dist${NC}"
    echo ""
    echo -e "${GREEN}🌐 После деплоя ваше приложение будет доступно по адресу Netlify${NC}"
else
    echo -e "${RED}❌ Ошибка при создании build${NC}"
    exit 1
fi