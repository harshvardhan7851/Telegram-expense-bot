from sqlalchemy import text
from database import engine


def add_expense(chat_id, description, amount):
    with engine.connect() as conn:
        conn.execute(
            text("""
            INSERT INTO expenses (chat_id, description, amount)
            VALUES (:chat_id, :description, :amount)
            """),
            {
                "chat_id": chat_id,
                "description": description,
                "amount": amount
            }
        )
        conn.commit()