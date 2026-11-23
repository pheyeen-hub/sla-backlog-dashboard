"""Generate a reproducible synthetic case dataset."""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = datetime(2025, 12, 31, 23, 59, 59)
START = datetime(2025, 1, 1)


def main():
    rng = random.Random(42)
    rows = []
    for number in range(1, 1501):
        created = START + timedelta(hours=rng.randrange(365 * 24))
        priority = rng.choices(["High", "Medium", "Low"], [0.2, 0.5, 0.3])[0]
        sla_hours = {"High": 24, "Medium": 72, "Low": 120}[priority]
        team = rng.choice(["North", "South", "Central"])
        category = rng.choice(["Access", "Billing", "Order", "Technical"])
        # Add variation between categories so the analysis has useful comparisons.
        multiplier = {"Access": 0.7, "Billing": 1.0, "Order": 0.9, "Technical": 1.3}[category]
        resolution_hours = max(1, round(rng.gammavariate(2, 0.45) * sla_hours * multiplier))
        resolved = created + timedelta(hours=resolution_hours)
        if resolved > SNAPSHOT or rng.random() < 0.07:
            resolved = None
        due = created + timedelta(hours=sla_hours)
        rows.append({
            "case_id": f"CASE-{number:04d}",
            "created_at": created.isoformat(sep=" "),
            "due_at": due.isoformat(sep=" "),
            "resolved_at": resolved.isoformat(sep=" ") if resolved else "",
            "team": team,
            "category": category,
            "priority": priority,
            "sla_hours": sla_hours,
        })

    path = ROOT / "data" / "cases.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic cases to {path}")


if __name__ == "__main__":
    main()
