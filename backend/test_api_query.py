#!/usr/bin/env python3
"""
Тестирование API без JOIN'ов
"""
import sys
import os

sys.path.insert(0, os.path.abspath("."))

from app.core.database import get_db
from app.models import Lot, LotStatus
from sqlalchemy.orm import Session


def test_api_query():
    """Тестируем запрос как в API, но без joinedload"""
    db: Session = next(get_db())

    try:
        # Такой же запрос как в API, но без joinedload
        query = db.query(Lot)
        query = query.filter(Lot.status == LotStatus.ACTIVE)

        # Получаем count
        total = query.count()
        print(f"Total count: {total}")

        # Получаем записи
        lots = query.order_by(Lot.created_at.desc()).limit(2).all()
        print(f"Retrieved lots: {len(lots)}")

        for lot in lots:
            print(f"Lot {lot.id}: {lot.title}")

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_api_query()
