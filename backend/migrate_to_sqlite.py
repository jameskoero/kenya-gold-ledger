"""
Migrates kenya-gold-ledger's existing CSV/JSON files into a single SQLite database
that the FastAPI backend serves from.

Run this from the repo root in Colab/Termux:
    python backend/migrate_to_sqlite.py

It expects the existing repo structure (data/*.csv, data/*.json) to be present.
It does NOT invent any rows -- if a source file is missing, that table is skipped
and a warning is printed, per the project's no-fabricated-data rule.
"""
import sqlite3
import csv
import json
import os
import sys

DB_PATH = "backend/kenya_gold_ledger.db"
DATA_DIR = "data"

CSV_TABLES = {
    "medals_by_games.csv": "medals_by_games",
    "golds.csv": "golds",
    "all_medals.csv": "all_medals",
    "policy_timeline.csv": "policy_timeline",
    "funding_vs_output.csv": "funding_vs_output",
    "governance_scorecard.csv": "governance_scorecard",
    "geo/kenya_counties.csv": "kenya_counties",
    "geo/medalist_origins.csv": "medalist_origins",
}

# json_path -> (table_name, records_key)
# records_key is the key holding the array inside the JSON file, or None if the
# file's top level IS the array.
JSON_TABLES = {
    "controversies.json": ("controversies", "records"),
    "sgo_framework.json": ("sgo_framework_dimensions", "dimensions"),
}


def load_csv_to_table(conn, path, table_name):
    if not os.path.exists(path):
        print(f"[skip] {path} not found -- table '{table_name}' not created.")
        return
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if not rows:
            print(f"[skip] {path} is empty.")
            return
        cols = rows[0].keys()
        col_defs = ", ".join(f'"{c}" TEXT' for c in cols)
        conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        conn.execute(f'CREATE TABLE "{table_name}" ({col_defs})')
        placeholders = ", ".join("?" for _ in cols)
        conn.executemany(
            f'INSERT INTO "{table_name}" VALUES ({placeholders})',
            [tuple(row[c] for c in cols) for row in rows],
        )
        print(f"[ok] {table_name}: {len(rows)} rows from {path}")


def load_json_to_table(conn, path, table_name, records_key=None):
    if not os.path.exists(path):
        print(f"[skip] {path} not found -- table '{table_name}' not created.")
        return
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    data = raw.get(records_key) if records_key else raw

    if not isinstance(data, list) or not data:
        print(f"[skip] {path} (key='{records_key}') is not a non-empty JSON array.")
        return

    cols = sorted({k for row in data for k in row.keys()})
    col_defs = ", ".join(f'"{c}" TEXT' for c in cols)
    conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    conn.execute(f'CREATE TABLE "{table_name}" ({col_defs})')
    placeholders = ", ".join("?" for _ in cols)
    for row in data:
        values = [
            json.dumps(row[c]) if isinstance(row.get(c), (dict, list)) else row.get(c)
            for c in cols
        ]
        conn.execute(f'INSERT INTO "{table_name}" VALUES ({placeholders})', values)
    print(f"[ok] {table_name}: {len(data)} rows from {path}")


def main():
    os.makedirs("backend", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    for rel_path, table in CSV_TABLES.items():
        load_csv_to_table(conn, os.path.join(DATA_DIR, rel_path), table)
    for rel_path, (table, key) in JSON_TABLES.items():
        load_json_to_table(conn, os.path.join(DATA_DIR, rel_path), table, key)
    conn.commit()
    conn.close()
    print(f"\nDone. Database written to {DB_PATH}")


if __name__ == "__main__":
    sys.exit(main())
