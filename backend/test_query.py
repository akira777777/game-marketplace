#!/usr/bin/env python3
"""
Тестирование прямого запроса к базе данных
"""
import sys
import os

sys.path.insert(0, os.path.abspath(".."))  # noqa: E402

from app.core.database import get_db  # noqa: E402
from app.models import Lot  # noqa: E402
from sqlalchemy.orm import Session


def test_query():
    """Тестируем запрос к базе"""
    db: Session = next(get_db())

    try:
        # Простой запрос всех лотов
        lots = db.query(Lot).all()
        print(f"Всего лотов: {len(lots)}")

        for lot in lots:
            print(f"ID: {lot.id}, Title: {lot.title}, Status: {lot.status}")

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_query()
