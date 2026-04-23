import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "chat.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name     TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_by    TEXT NOT NULL,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            username  TEXT NOT NULL,
            message   TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def create_room(room_name, password, created_by):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO rooms (room_name, password_hash, created_by) VALUES (?, ?, ?)",
            (room_name, hashed, created_by)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_room(room_name, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM rooms WHERE room_name = ?", (room_name,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return "not_found"
    if check_password_hash(row["password_hash"], password):
        return "ok"
    return "wrong_password"

def save_message(room_name, username, message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (room_name, username, message) VALUES (?, ?, ?)",
        (room_name, username, message)
    )
    conn.commit()
    conn.close()

def get_recent_messages(room_name, limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT username, message, timestamp FROM messages
           WHERE room_name = ?
           ORDER BY id DESC LIMIT ?""",
        (room_name, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return list(reversed([dict(row) for row in rows]))