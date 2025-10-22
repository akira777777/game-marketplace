#!/usr/bin/env python3
"""
Простой скрипт для добавления тестовых данных
"""
import sys
import os

sys.path.insert(0, os.path.abspath("."))

from app.core.database import get_db
from app.models import User, Game, Lot
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_simple_test_data():
    """Создает простые тестовые данные"""
    db: Session = next(get_db())

    try:
        # Создаем тестового пользователя
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            test_user = User(
                username="testuser",
                email="test@example.com",
                hashed_password=pwd_context.hash("testpass123"),
                is_active=True,
                display_name="Test User",
                bio="Тестовый пользователь для демонстрации",
            )
            db.add(test_user)
            db.flush()

        # Создаем игры
        games_data = [
            {
                "name": "World of Warcraft",
                "description": "Легендарная MMORPG от Blizzard Entertainment",
                "image_url": "https://bnetcmsus-a.akamaihd.net/cms/gallery/IUTVP1WBIG861541788064302.jpg",
            },
            {
                "name": "Counter-Strike 2",
                "description": "Культовый командный шутер",
                "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/730/header.jpg",
            },
            {
                "name": "Dota 2",
                "description": "Самая популярная MOBA игра",
                "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/570/header.jpg",
            },
            {
                "name": "The Witcher 3",
                "description": "Эпическая RPG о ведьмаке Геральте",
                "image_url": "https://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg",
            },
        ]

        games = []
        for game_data in games_data:
            game = db.query(Game).filter(Game.name == game_data["name"]).first()
            if not game:
                game = Game(**game_data, is_active=True)
                db.add(game)
                db.flush()
            games.append(game)

        # Создаем тестовые лоты (без категорий пока)
        lots_data = [
            {
                "title": "Аккаунт WoW с редкими маунтами",
                "description": "Аккаунт в World of Warcraft с коллекцией редких маунтов и достижений. Играл с самого начала! Включает редкого дракона времени и множество эксклюзивных предметов.",
                "price": 15000,
                "game_id": games[0].id,
                "seller_id": test_user.id,
                "status": "active",
                "category_id": 1,  # dummy category
            },
            {
                "title": "CS2 Prime аккаунт Global Elite",
                "description": "Аккаунт Counter-Strike 2 с рангом Global Elite, много дорогих скинов, Prime статус. Идеальная статистика.",
                "price": 8500,
                "game_id": games[1].id,
                "seller_id": test_user.id,
                "status": "active",
                "category_id": 1,  # dummy category
            },
            {
                "title": "Dota 2 аккаунт Divine ранга",
                "description": "Аккаунт Dota 2 с рангом Divine, большая коллекция Immortal предметов, редкие сеты героев.",
                "price": 12000,
                "game_id": games[2].id,
                "seller_id": test_user.id,
                "status": "active",
                "category_id": 1,  # dummy category
            },
            {
                "title": "The Witcher 3 полное прохождение + DLC",
                "description": "Сохранение игры с 100% прохождением основной игры и всех DLC. Все квесты, сокровища и секреты открыты.",
                "price": 500,
                "game_id": games[3].id,
                "seller_id": test_user.id,
                "status": "active",
                "category_id": 1,  # dummy category
            },
        ]

        for lot_data in lots_data:
            existing_lot = db.query(Lot).filter(Lot.title == lot_data["title"]).first()
            if not existing_lot:
                lot = Lot(**lot_data)
                db.add(lot)

        db.commit()
        print("✅ Тестовые данные успешно добавлены!")
        print(f"🎮 Создано игр: {len(games)}")
        print(f"📦 Создано лотов: {len(lots_data)}")
        print("👤 Тестовый пользователь: test@example.com / testpass123")

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_simple_test_data()
