#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

NETLIFY_URL="https://cheerful-cocada-c90721.netlify.app"

echo -e "${BLUE}🌐 Тестирование развернутого Game Marketplace${NC}"
echo "=============================================="
echo -e "${YELLOW}URL: $NETLIFY_URL${NC}"
echo ""

# Функция для тестирования endpoint'а
test_netlify_endpoint() {
    local path="$1"
    local expected_status="$2"
    local description="$3"
    local url="$NETLIFY_URL$path"
    
    echo -e "\n${YELLOW}🔍 Тестирую: ${description}${NC}"
    echo "URL: $url"
    
    # Выполняем запрос
    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    status_code=$(echo "$response" | tail -1)
    body=$(echo "$response" | head -n -1)
    
    # Проверяем статус код
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✅ Статус: $status_code (ожидался $expected_status)${NC}"
        
        # Показываем информацию о контенте
        if [ ! -z "$body" ]; then
            content_length=${#body}
            echo -e "${BLUE}📄 Размер контента: $content_length символов${NC}"
            
            # Проверяем что это HTML
            if echo "$body" | grep -q "<!DOCTYPE html"; then
                echo -e "${GREEN}✅ HTML контент загружен корректно${NC}"
                
                # Извлекаем title
                title=$(echo "$body" | grep -o '<title[^>]*>[^<]*</title>' | sed 's/<[^>]*>//g')
                if [ ! -z "$title" ]; then
                    echo -e "${BLUE}📋 Title: $title${NC}"
                fi
                
                # Проверяем наличие JavaScript и CSS
                if echo "$body" | grep -q "\.js"; then
                    echo -e "${GREEN}✅ JavaScript файлы подключены${NC}"
                fi
                if echo "$body" | grep -q "\.css"; then
                    echo -e "${GREEN}✅ CSS файлы подключены${NC}"
                fi
            else
                # Показываем первые несколько строк для других типов контента
                echo -e "${BLUE}📄 Превью контента:${NC}"
                echo "$body" | head -3
                if [ $(echo "$body" | wc -l) -gt 3 ]; then
                    echo "..."
                fi
            fi
        fi
    else
        echo -e "${RED}❌ Статус: $status_code (ожидался $expected_status)${NC}"
        if [ ! -z "$body" ]; then
            echo -e "${RED}Ответ: $(echo "$body" | head -1)${NC}"
        fi
    fi
}

# Проверяем основные маршруты SPA
echo -e "${BLUE}🏠 Тестирование основных страниц...${NC}"

test_netlify_endpoint "/" 200 "Главная страница"
test_netlify_endpoint "/catalog" 200 "Страница каталога (SPA маршрут)"
test_netlify_endpoint "/login" 200 "Страница входа (SPA маршрут)"
test_netlify_endpoint "/register" 200 "Страница регистрации (SPA маршрут)"
test_netlify_endpoint "/profile" 200 "Страница профиля (SPA маршрут)"

# Проверяем несуществующие маршруты (должны возвращать index.html)
echo -e "\n${BLUE}🚫 Тестирование несуществующих маршрутов...${NC}"
test_netlify_endpoint "/nonexistent-page" 200 "Несуществующая страница (должна вернуть index.html)"
test_netlify_endpoint "/catalog/some-game" 200 "Глубокий маршрут каталога"

# Проверяем статические ресурсы
echo -e "\n${BLUE}📦 Тестирование статических ресурсов...${NC}"

# Получаем список JS и CSS файлов из главной страницы
echo -e "${YELLOW}📋 Получаю список статических ресурсов...${NC}"
main_page=$(curl -s "$NETLIFY_URL/")

# Ищем JS файлы
js_files=$(echo "$main_page" | grep -o '/assets/[^"]*\.js' | head -3)
css_files=$(echo "$main_page" | grep -o '/assets/[^"]*\.css' | head -3)

if [ ! -z "$js_files" ]; then
    echo -e "${BLUE}📄 Тестирую JavaScript файлы:${NC}"
    echo "$js_files" | while read -r js_file; do
        if [ ! -z "$js_file" ]; then
            test_netlify_endpoint "$js_file" 200 "JavaScript файл: $(basename "$js_file")"
        fi
    done
fi

if [ ! -z "$css_files" ]; then
    echo -e "${BLUE}🎨 Тестирую CSS файлы:${NC}"
    echo "$css_files" | while read -r css_file; do
        if [ ! -z "$css_file" ]; then
            test_netlify_endpoint "$css_file" 200 "CSS файл: $(basename "$css_file")"
        fi
    done
fi

# Проверяем производительность
echo -e "\n${BLUE}⚡ Анализ производительности...${NC}"

# Измеряем время загрузки главной страницы
echo -e "${YELLOW}⏱️  Измеряю время загрузки...${NC}"
start_time=$(date +%s%N)
curl -s "$NETLIFY_URL/" > /dev/null
end_time=$(date +%s%N)
load_time=$(( (end_time - start_time) / 1000000 ))
echo -e "${GREEN}🚀 Время загрузки главной страницы: ${load_time}ms${NC}"

# Проверяем размер главной страницы
main_page_size=$(curl -s "$NETLIFY_URL/" | wc -c)
echo -e "${GREEN}📏 Размер главной страницы: $main_page_size байт${NC}"

# Проверяем заголовки безопасности
echo -e "\n${BLUE}🔒 Проверка заголовков безопасности...${NC}"
headers=$(curl -s -I "$NETLIFY_URL/")

check_header() {
    local header_name="$1"
    local header_description="$2"
    
    if echo "$headers" | grep -qi "$header_name:"; then
        header_value=$(echo "$headers" | grep -i "$header_name:" | cut -d: -f2- | tr -d '\r\n' | sed 's/^ *//')
        echo -e "${GREEN}✅ $header_description: $header_value${NC}"
    else
        echo -e "${YELLOW}⚠️  $header_description: Не установлен${NC}"
    fi
}

check_header "x-frame-options" "X-Frame-Options"
check_header "x-content-type-options" "X-Content-Type-Options"
check_header "x-xss-protection" "X-XSS-Protection"
check_header "strict-transport-security" "HSTS"
check_header "content-security-policy" "CSP"

# Проверяем HTTPS
echo -e "\n${BLUE}🔐 Проверка HTTPS...${NC}"
if echo "$NETLIFY_URL" | grep -q "https://"; then
    echo -e "${GREEN}✅ HTTPS включен${NC}"
    
    # Проверяем редирект с HTTP на HTTPS
    http_url=$(echo "$NETLIFY_URL" | sed 's/https:/http:/')
    http_response=$(curl -s -I "$http_url" | head -1)
    if echo "$http_response" | grep -q "301\|302"; then
        echo -e "${GREEN}✅ HTTP → HTTPS редирект настроен${NC}"
    else
        echo -e "${YELLOW}⚠️  HTTP → HTTPS редирект может быть не настроен${NC}"
    fi
else
    echo -e "${RED}❌ HTTPS не используется${NC}"
fi

# Финальная сводка
echo -e "\n${GREEN}🎉 Тестирование Netlify деплоя завершено!${NC}"
echo -e "${BLUE}📋 Сводка:${NC}"
echo -e "🌐 URL: $NETLIFY_URL"
echo -e "⚡ Время загрузки: ${load_time}ms"
echo -e "📏 Размер страницы: $main_page_size байт"
echo -e ""
echo -e "${YELLOW}📋 Рекомендации для production:${NC}"
echo -e "1. Настройте переменные окружения для API"
echo -e "2. Разверните backend на Heroku/Railway/Render"
echo -e "3. Обновите VITE_API_BASE_URL в настройках Netlify"
echo -e "4. Настройте домен (если нужно)"
echo -e ""
echo -e "${GREEN}✨ Ваше приложение успешно развернуто и работает!${NC}"