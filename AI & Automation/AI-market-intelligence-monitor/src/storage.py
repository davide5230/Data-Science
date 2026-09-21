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

def save_report(
    query,
    statistics,
    report
):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    cursor.execute(
        """
        INSERT INTO reports (
            created_at,
            query,
            statistics,
            report
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            created_at,
            query,
            json.dumps(statistics),
            report.model_dump_json()
        )
    )

    connection.commit()
    connection.close()
