import sqlite3
import json
from datetime import datetime, timezone


DB_PATH = "data/market_intelligence.db"


def init_database():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            query TEXT NOT NULL,
            statistics TEXT NOT NULL,
            report TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()
