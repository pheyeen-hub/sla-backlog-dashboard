# SLA and backlog dashboard

A personal portfolio project using **synthetic data** to explore case volumes, SLA compliance, resolution time, and overdue work. The data and findings do not represent a real employer or customers.

The project is a starting point: the CSV, Python generator, and SQLite analysis are included; the Power BI report must be built in Power BI Desktop using the guide below. Do not claim to have built the report until you have completed it yourself.

## What this project answers

- What percentage of resolved cases met their SLA?
- How many cases remain open or overdue at the snapshot?
- Which teams and case categories have the most SLA breaches?
- How do case volumes and resolution times vary by month?

## Files

- `data/cases.csv` — 1,500 synthetic cases, captured as of **2025-12-31 23:59:59**.
- `scripts/generate_data.py` — reproducible, standard-library-only data generator.
- `sql/analysis.sql` — SQLite queries for the project questions.
- `scripts/run_analysis.py` — loads the CSV into an in-memory SQLite database and runs the queries.
- `POWER_BI_GUIDE.md` — step-by-step dashboard and publishing instructions.

## Run the SQL analysis

Install Python 3, open a terminal in the project folder, and run:

```bash
python scripts/run_analysis.py
```

On Windows, use `py scripts/run_analysis.py` if `python` is unavailable. The script uses Python's built-in SQLite library; no database setup or packages are required. To regenerate the data, run `python scripts/generate_data.py`.

The unfiltered baseline is **1,500 cases**, **67.9% resolved SLA compliance**, **115 open cases**, and **103 open overdue cases**. Technical cases have the most SLA breaches in each team in this simulated dataset. Run the queries and explore the results yourself before presenting them.

## Data and definitions

Each row represents one case. Dates and times are synthetic and use calendar hours rather than business hours. An SLA deadline is `created_at` plus the target hours for the case priority. There are no pauses or excluded holidays.

| Column | Meaning |
| --- | --- |
| `case_id` | Unique case identifier |
| `created_at` | Case creation date and time |
| `due_at` | SLA deadline |
| `resolved_at` | Resolution date and time; blank if still open at the snapshot |
| `team` | Team responsible for the case |
| `category` | Type of case |
| `priority` | Case priority |
| `sla_hours` | Time allowed before the SLA deadline |

**Resolved SLA compliance** is resolved cases completed on or before `due_at`, divided by all resolved cases. Open cases are excluded from this rate; open cases past their deadline are counted separately as overdue. **Open backlog** is the number of cases unresolved at the snapshot, not a historical trend. Average resolution time includes resolved cases only.

## Next steps

Follow [the Power BI guide](POWER_BI_GUIDE.md) on a Windows computer, save the `.pbix` file, and add it and a screenshot to this repository. Replace the following example with your own verified work and findings:

> **SLA and Backlog Dashboard | Personal Project** — Analyzed synthetic case data with SQL and built a Power BI dashboard showing SLA compliance, open backlog, and resolution trends.

Only describe work you have completed, and use actual calculated results rather than claiming business improvements from synthetic data.
