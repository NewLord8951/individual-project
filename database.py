import sqlite3
from typing import List, Tuple, Optional
from contextlib import contextmanager


@contextmanager
def db_connection():
    """Контекстный менеджер для работы с базой данных."""
    conn = sqlite3.connect("bot.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Инициализация базы данных и создание таблиц."""
    with db_connection() as conn:
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
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
        )
        """)

        conn.commit()


def add_user(user_id: int, username: Optional[str] = None, full_name: Optional[str] = None):
    """Добавляет пользователя в базу данных."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
            (user_id, username, full_name)
        )
        conn.commit()


def add_warning(user_id: int, admin_id: int, reason: str = "") -> bool:
    """Добавляет предупреждение пользователю."""
    try:
        with db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
            if not cursor.fetchone():
                return False

            cursor.execute(
                "INSERT INTO warnings (user_id, admin_id, reason) VALUES (?, ?, ?)",
                (user_id, admin_id, reason)
            )

            cursor.execute(
                "UPDATE users SET warnings = warnings + 1 WHERE user_id = ?",
                (user_id,)
            )

            conn.commit()
            return True
    except sqlite3.Error:
        return False


def get_warnings(user_id: int) -> int:
    """Возвращает количество предупреждений пользователя."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT warnings FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        return result["warnings"] if result else 0


def get_warnings_history(user_id: int) -> List[Tuple]:
    """Возвращает историю предупреждений пользователя."""
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT w.id, w.admin_id, u.username as admin_username, 
                   w.reason, w.timestamp 
            FROM warnings w
            LEFT JOIN users u ON w.admin_id = u.user_id
            WHERE w.user_id = ?
            ORDER BY w.timestamp DESC
            """,
            (user_id,)
        )
        return cursor.fetchall()


def remove_warning(warning_id: int) -> bool:
    """Удаляет предупреждение по его ID."""
    try:
        with db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT user_id FROM warnings WHERE id = ?", (warning_id,))
            result = cursor.fetchone()
            if not result:
                return False

            user_id = result["user_id"]

            cursor.execute("DELETE FROM warnings WHERE id = ?", (warning_id,))

            cursor.execute(
                "UPDATE users SET warnings = GREATEST(0, warnings - 1) WHERE user_id = ?",
                (user_id,)
            )

            conn.commit()
            return True
    except sqlite3.Error:
        return False
