#!/usr/bin/env python3
"""
Скрипт для добавления тестовых данных в базу GameMarketplace
"""
import sys
import os

sys.path.insert(0, os.path.abspath("."))

from app.core.database import get_db
from app.models import User, Game, Category, Lot
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_test_data():
    """Создает тестовые данные для демонстрации"""
    db: Session = next(get_db())

    try:
        # Создаем категории игр
        categories_data = [
            {
                "name": "MMORPG",
                "description": "Массовые многопользовательские онлайн-игры",
            },
            {"name": "FPS", "description": "Шутеры от первого лица"},
            {"name": "MOBA", "description": "Многопользовательские боевые арены"},
            {"name": "RPG", "description": "Ролевые игры"},
            {"name": "Strategy", "description": "Стратегические игры"},
        ]

        categories = []
        for cat_data in categories_data:
            category = (
                db.query(Category).filter(Category.name == cat_data["name"]).first()
            )
            if not category:
                category = Category(**cat_data)
                db.add(category)
                db.flush()
            categories.append(category)

        # Создаем игры
        games_data = [
            {
                "name": "World of Warcraft",
                "description": "Легендарная MMORPG от Blizzard Entertainment",
                "category_id": categories[0].id,
                "image_url": "https://images.blz-contentstack.com/v3/assets/blt2477dcaf4ebd440c/blt3c650c6c0827a078/wow-classic-hardcore-meta-image.jpg",
            },
            {
                "name": "Counter-Strike 2",
                "description": "Культовый командный шутер",
                "category_id": categories[1].id,
                "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg",
            },
            {
                "name": "Dota 2",
                "description": "Самая популярная MOBA игра",
                "category_id": categories[2].id,
                "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/570/header.jpg",
            },
            {
                "name": "The Witcher 3",
                "description": "Эпическая RPG о ведьмаке Геральте",
                "category_id": categories[3].id,
                "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg",
            },
            {
                "name": "Civilization VI",
                "description": "Пошаговая стратегия о развитии цивилизации",
                "category_id": categories[4].id,
                "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/289070/header.jpg",
            },
        ]

        games = []
        for game_data in games_data:
            game = db.query(Game).filter(Game.name == game_data["name"]).first()
            if not game:
                game = Game(**game_data)
                db.add(game)
                db.flush()
            games.append(game)

        # Создаем тестового пользователя
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            test_user = User(
                username="testuser",
                email="test@example.com",
                hashed_password=pwd_context.hash("testpass123"),
                is_active=True,
            )
            db.add(test_user)
            db.flush()

        # Создаем тестовые лоты
        lots_data = [
            {
                "title": "Аккаунт WoW с редкими маунтами",
                "description": "Аккаунт в World of Warcraft с коллекцией редких маунтов и достижений. Играл с самого начала!",
                "price": 15000,
                "game_id": games[0].id,
                "seller_id": test_user.id,
                "status": "active",
            },
            {
                "title": "CS2 Prime аккаунт Global Elite",
                "description": "Аккаунт Counter-Strike 2 с рангом Global Elite, много скинов, Prime статус",
                "price": 8500,
                "game_id": games[1].id,
                "seller_id": test_user.id,
                "status": "active",
            },
            {
                "title": "Dota 2 аккаунт Divine ранга",
                "description": "Аккаунт Dota 2 с рангом Divine, большая коллекция предметов и Immortal items",
                "price": 12000,
                "game_id": games[2].id,
                "seller_id": test_user.id,
                "status": "active",
            },
            {
                "title": "The Witcher 3 полное прохождение",
                "description": "Сохранение игры с 100% прохождением, все квесты, DLC и секреты открыты",
                "price": 500,
                "game_id": games[3].id,
                "seller_id": test_user.id,
                "status": "active",
            },
            {
                "title": "Civilization VI + все DLC",
                "description": "Лицензионная копия Civilization VI со всеми дополнениями и сценариями",
                "price": 2500,
                "game_id": games[4].id,
                "seller_id": test_user.id,
                "status": "active",
            },
        ]

        for lot_data in lots_data:
            existing_lot = db.query(Lot).filter(Lot.title == lot_data["title"]).first()
            if not existing_lot:
                lot = Lot(**lot_data)
                db.add(lot)

        db.commit()
        print("✅ Тестовые данные успешно добавлены!")
        print(f"📊 Создано категорий: {len(categories)}")
        print(f"🎮 Создано игр: {len(games)}")
        print(f"📦 Создано лотов: {len(lots_data)}")
        print(f"👤 Тестовый пользователь: test@example.com / testpass123")

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании тестовых данных: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()
