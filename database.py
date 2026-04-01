import sqlite3
import hashlib

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    favorites TEXT,
    genres TEXT
)
""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            (username, hash_password(password), "", "")
        )
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    return cursor.fetchone()

def save_preferences(username, favorites, genres):
    cursor.execute(
        "UPDATE users SET favorites=?, genres=? WHERE username=?",
        ("|".join(favorites), "|".join(genres), username)
    )
    conn.commit()

def get_preferences(username):
    cursor.execute(
        "SELECT favorites, genres FROM users WHERE username=?",
        (username,)
    )
    result = cursor.fetchone()

    favs = result[0].split("|") if result and result[0] else []
    genres = result[1].split("|") if result and result[1] else []

    return favs, genres