import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DB_PATH = DATA_DIR / "market_intelligence.db"


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
    print(f"Saving database to: {DB_PATH}")

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

    print(
        f"Rows saved: "
        f"{cursor.execute('SELECT COUNT(*) FROM reports').fetchone()[0]}"
    )

    connection.close()

def get_reports():
    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            created_at,
            query,
            statistics,
            report
        FROM reports
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]

    

    connection.commit()
    connection.close()
