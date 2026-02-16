import sqlite3
from pathlib import Path

DB_PATH = Path("expenses.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def get_or_create_user(username: str) -> int:
    username = username.strip().lower()
    if not username:
        raise ValueError("username vazio")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row:
        conn.close()
        return row["id"]

    cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def add_expense_db(user_id: int, amount: float, description: str, category: str, date_str: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (user_id, amount, description, category, date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, float(amount), description.strip(), category.strip().lower(), date_str),
    )

    conn.commit()
    conn.close()


def list_expenses_db(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, amount, description, category, date
        FROM expenses
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def remove_expense_db(user_id: int, expense_id: int) -> int:
    """Remove e retorna quantas linhas foram removidas (0 ou 1)."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE user_id = ? AND id = ?",
        (user_id, int(expense_id)),
    )

    conn.commit()
    removed = cursor.rowcount
    conn.close()
    return removed
