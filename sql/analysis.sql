-- Snapshot KPIs. Compliance considers resolved cases only.
SELECT
    COUNT(*) AS total_cases,
    COUNT(resolved_at) AS resolved_cases,
    SUM(CASE WHEN resolved_at IS NULL THEN 1 ELSE 0 END) AS open_backlog,
    SUM(CASE WHEN resolved_at IS NULL AND due_at < '2025-12-31 23:59:59' THEN 1 ELSE 0 END) AS open_overdue,
    ROUND(100.0 * SUM(CASE WHEN resolved_at IS NOT NULL AND resolved_at <= due_at THEN 1 ELSE 0 END)
        / NULLIF(COUNT(resolved_at), 0), 1) AS resolved_sla_pct,
    ROUND(AVG((julianday(resolved_at) - julianday(created_at)) * 24), 1) AS avg_resolution_hours
FROM cases;

-- Compare teams and case categories using resolved cases.
SELECT
    team,
    category,
    COUNT(*) AS resolved_cases,
    SUM(CASE WHEN resolved_at > due_at THEN 1 ELSE 0 END) AS sla_breaches,
    ROUND(100.0 * SUM(CASE WHEN resolved_at <= due_at THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1) AS resolved_sla_pct
FROM cases
WHERE resolved_at IS NOT NULL
GROUP BY team, category
ORDER BY sla_breaches DESC, team, category;

-- Monthly cohorts: resolution metrics refer to cases created in that month.
SELECT
    substr(created_at, 1, 7) AS created_month,
    COUNT(*) AS cases_created,
    COUNT(resolved_at) AS resolved_cases,
    ROUND(AVG((julianday(resolved_at) - julianday(created_at)) * 24), 1) AS avg_resolution_hours
FROM cases
GROUP BY substr(created_at, 1, 7)
ORDER BY created_month;
