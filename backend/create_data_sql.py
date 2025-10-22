import sqlite3
import hashlib


def create_test_data():
    """Создает тестовые данные через прямые SQL запросы"""
    conn = sqlite3.connect("gamemarket.db")
    cursor = conn.cursor()

    try:
        # Создаем тестового пользователя
        hashed_password = hashlib.sha256("testpass123".encode()).hexdigest()

        # Проверяем, есть ли уже пользователь
        cursor.execute("SELECT id FROM users WHERE email = ?", ("test@example.com",))
        user = cursor.fetchone()

        if not user:
            cursor.execute(
                """
                INSERT INTO users (username, email, hashed_password, is_active, display_name, bio)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    "testuser",
                    "test@example.com",
                    hashed_password,
                    True,
                    "Тестовый пользователь",
                    "Опытный продавец игровых аккаунтов",
                ),
            )
            user_id = cursor.lastrowid
        else:
            user_id = user[0]

        # Создаем игры
        games_data = [
            ("World of Warcraft", "Культовая MMORPG от Blizzard", True),
            ("Counter-Strike 2", "Легендарный шутер", True),
            ("Dota 2", "Популярная MOBA", True),
            ("Valorant", "Тактический шутер от Riot", True),
        ]

        game_ids = []
        for name, description, is_active in games_data:
            cursor.execute("SELECT id FROM games WHERE name = ?", (name,))
            game = cursor.fetchone()

            if not game:
                cursor.execute(
                    """
                    INSERT INTO games (name, description, is_active)
                    VALUES (?, ?, ?)
                """,
                    (name, description, is_active),
                )
                game_ids.append(cursor.lastrowid)
            else:
                game_ids.append(game[0])

        # Создаем категории для каждой игры
        category_ids = []
        for i, game_id in enumerate(game_ids):
            cursor.execute(
                "SELECT id FROM categories WHERE name = ? AND game_id = ?",
                ("Аккаунты", game_id),
            )
            category = cursor.fetchone()

            if not category:
                cursor.execute(
                    """
                    INSERT INTO categories (name, description, game_id, is_active)
                    VALUES (?, ?, ?, ?)
                """,
                    ("Аккаунты", "Игровые аккаунты", game_id, True),
                )
                category_ids.append(cursor.lastrowid)
            else:
                category_ids.append(category[0])

        # Создаем лоты
        lots_data = [
            (
                "WoW аккаунт с редкими маунтами",
                "Аккаунт с коллекцией редких маунтов",
                15000,
                game_ids[0],
                category_ids[0],
            ),
            (
                "CS2 Prime Global Elite",
                "Аккаунт с рангом Global Elite",
                8500,
                game_ids[1],
                category_ids[1],
            ),
            (
                "Dota 2 Divine аккаунт",
                "Высокий ранг Divine",
                12000,
                game_ids[2],
                category_ids[2],
            ),
            (
                "Valorant Immortal ранг",
                "Аккаунт с рангом Immortal",
                7500,
                game_ids[3],
                category_ids[3],
            ),
        ]

        for title, description, price, game_id, cat_id in lots_data:
            cursor.execute("SELECT id FROM lots WHERE title = ?", (title,))
            lot = cursor.fetchone()

            if not lot:
                cursor.execute(
                    """
                    INSERT INTO lots (title, description, price, game_id, seller_id, category_id, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        title,
                        description,
                        price,
                        game_id,
                        user_id,
                        cat_id,
                        "active",
                    ),
                )

        conn.commit()
        print("✅ Тестовые данные созданы!")
        print(f"👤 Пользователь: test@example.com / testpass123")
        print(f"🎮 Игр: {len(game_ids)}")
        print(f"📦 Лотов: {len(lots_data)}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка: {e}")
        import traceback

        traceback.print_exc()
    finally:
        conn.close()


if __name__ == "__main__":
    create_test_data()
