import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "market_intelligence.db"


def init_database():
    with sqlite3.connect(DB_PATH) as connection:
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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seen_articles (
                article_id TEXT PRIMARY KEY,
                url TEXT,
                first_seen_at TEXT NOT NULL
            )
        """)


def save_report(
    query,
    statistics,
    report
):
    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
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


def get_reports():
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute("""
            SELECT
                id,
                created_at,
                query,
                statistics,
                report
            FROM reports
            ORDER BY created_at DESC
        """).fetchall()

    return [
        dict(row)
        for row in rows
    ]


def get_seen_article_ids():
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute("""
            SELECT article_id
            FROM seen_articles
        """).fetchall()

    return {
        row[0]
        for row in rows
    }


def save_seen_articles(articles):
    if not articles:
        return

    now = datetime.now(
        timezone.utc
    ).isoformat()

    records = [
        (
            article["article_id"],
            article["url"],
            now
        )
        for article in articles
    ]

    with sqlite3.connect(DB_PATH) as connection:
        connection.executemany(
            """
            INSERT OR IGNORE INTO seen_articles (
                article_id,
                url,
                first_seen_at
            )
            VALUES (?, ?, ?)
            """,
            records
        )
