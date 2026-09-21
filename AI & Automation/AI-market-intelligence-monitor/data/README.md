# Data

Runtime SQLite databases are stored in this directory.

The application uses `market_intelligence.db` to persist:

- generated market-intelligence reports;
- report statistics;
- article IDs that were successfully analyzed, enabling cross-run deduplication.

Runtime database files are excluded from version control.
