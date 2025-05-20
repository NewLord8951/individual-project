import sqlite3
from typing import List, Tuple


def init_db():
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        warnings INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        admin_id INTEGER,
        reason TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id: int, username: str, full_name: str):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
        (user_id, username, full_name)
    )
    conn.commit()
    conn.close()


def add_warning(user_id: int, admin_id: int, reason: str = ""):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO warnings (user_id, admin_id, reason) VALUES (?, ?, ?)",
        (user_id, admin_id, reason)
    )

    cursor.execute(
        "UPDATE users SET warnings = warnings + 1 WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()


def get_warnings(user_id: int) -> int:
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT warnings FROM users WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def get_warnings_history(user_id: int) -> List[Tuple]:
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT admin_id, reason, timestamp FROM warnings WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchall()
    conn.close()
    return result
