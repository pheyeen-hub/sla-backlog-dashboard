"""Load the project CSV into SQLite and print each analysis query."""

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    with sqlite3.connect(":memory:") as connection:
        connection.execute(
            """CREATE TABLE cases (
                case_id TEXT PRIMARY KEY, created_at TEXT NOT NULL,
                due_at TEXT NOT NULL, resolved_at TEXT, team TEXT NOT NULL,
                category TEXT NOT NULL, priority TEXT NOT NULL, sla_hours INTEGER NOT NULL
            )"""
        )
        with (ROOT / "data" / "cases.csv").open(newline="", encoding="utf-8") as file:
            rows = [
                (r["case_id"], r["created_at"], r["due_at"], r["resolved_at"] or None,
                 r["team"], r["category"], r["priority"], int(r["sla_hours"]))
                for r in csv.DictReader(file)
            ]
        connection.executemany("INSERT INTO cases VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)
        statement = ""
        for line in (ROOT / "sql" / "analysis.sql").read_text(encoding="utf-8").splitlines(True):
            statement += line
            if sqlite3.complete_statement(statement):
                cursor = connection.execute(statement)
                if cursor.description:
                    print("\n" + " | ".join(column[0] for column in cursor.description))
                    for row in cursor:
                        print(" | ".join(str(value) if value is not None else "N/A" for value in row))
                statement = ""
        if statement.strip():
            raise ValueError("SQL file ends with an incomplete statement")


if __name__ == "__main__":
    main()
