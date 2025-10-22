#!/usr/bin/env python3
"""
Скрипт для добавления тестовых данных с простым хешированием
"""
import sys
import os
import hashlib

sys.path.insert(0, os.path.abspath("."))

from app.core.database import get_db
from app.models import User, Game, Lot
from sqlalchemy.orm import Session


def simple_hash(password: str) -> str:
    """Простое хеширование для тестов"""
    return hashlib.sha256(password.encode()).hexdigest()


def create_test_data():
    """Создает тестовые данные"""
    db: Session = next(get_db())

    try:
        # Создаем тестового пользователя
        test_user = db.query(User).filter(User.email == "test@example.com").first()
        if not test_user:
            test_user = User(
                username="testuser",
                email="test@example.com",
                hashed_password=simple_hash("testpass123"),
                is_active=True,
                display_name="Тестовый пользователь",
                bio="Опытный продавец игровых аккаунтов",
            )
            db.add(test_user)
            db.flush()

        # Создаем игры
        games_data = [
            {
                "name": "World of Warcraft",
                "description": "Культовая MMORPG от Blizzard",
                "is_active": True,
            },
            {
                "name": "Counter-Strike 2",
                "description": "Легендарный шутер",
                "is_active": True,
            },
            {"name": "Dota 2", "description": "Популярная MOBA", "is_active": True},
            {
                "name": "Valorant",
                "description": "Тактический шутер от Riot",
                "is_active": True,
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

        # Создаем тестовые лоты (без категорий)
        lots_data = [
            {
                "title": "WoW аккаунт с редкими маунтами",
                "description": "Аккаунт с коллекцией редких маунтов и достижений",
                "price": 15000,
                "game_id": games[0].id,
                "seller_id": test_user.id,
                "status": "active",
                "category_id": 1,  # временное значение
            },
            {
                "title": "CS2 Prime Global Elite",
                "description": "Аккаунт с рангом Global Elite и множеством скинов",
                "price": 8500,
                "game_id": games[1].id,
                "seller_id": test_user.id,
                "status": "active",
                "category_id": 1,
            },
            {
                "title": "Dota 2 Divine аккаунт",
                "description": "Высокий ранг Divine с редкими предметами",
                "price": 12000,
                "game_id": games[2].id,
                "seller_id": test_user.id,
                "status": "active",
                "category_id": 1,
            },
            {
                "title": "Valorant Immortal ранг",
                "description": "Аккаунт с рангом Immortal, отличная статистика",
                "price": 7500,
                "game_id": games[3].id,
                "seller_id": test_user.id,
                "status": "active",
                "category_id": 1,
            },
        ]

        for lot_data in lots_data:
            existing = db.query(Lot).filter(Lot.title == lot_data["title"]).first()
            if not existing:
                lot = Lot(**lot_data)
                db.add(lot)

        db.commit()
        print("✅ Данные созданы!")
        print(f"🎮 Игр: {len(games)}")
        print(f"📦 Лотов: {len(lots_data)}")
        print("👤 Пользователь: test@example.com / testpass123")

    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data()
