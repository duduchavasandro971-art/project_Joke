
import sqlite3

def create_database():
    conn = sqlite3.connect("jokes.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jokes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            joke TEXT,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_joke(category, joke, date):
    conn = sqlite3.connect("jokes.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO jokes (category, joke, date) VALUES (?, ?, ?)",
        (category, joke, date)
    )

    conn.commit()
    conn.close()


def get_jokes():
    conn = sqlite3.connect("jokes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jokes ORDER BY id DESC")
    jokes = cursor.fetchall()

    conn.close()
    return jokes


def delete_joke(joke_id):
    conn = sqlite3.connect("jokes.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jokes WHERE id = ?", (joke_id,))

    conn.commit()
    conn.close()
