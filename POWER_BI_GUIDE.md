# Build the Power BI report

This guide uses the included synthetic CSV. The report is not yet included; create it in Power BI Desktop on Windows. All metrics are for the fixed snapshot **2025-12-31 23:59:59**.

## 1. Get the project

On the repository's GitHub page, select **Code > Download ZIP**, then extract it. Install and open Power BI Desktop. Select **Home > Get data > Text/CSV**, choose `data/cases.csv`, then select **Transform Data**.

In Power Query, confirm that `created_at`, `due_at`, and `resolved_at` are **Date/Time**; `sla_hours` is **Whole Number**; and the remaining columns are **Text**. Empty `resolved_at` values should be `null`. Rename the query to `Cases` and select **Close & Apply**.

## 2. Add measures

In the Data pane, select `Cases`. For each measure, select **Modeling > New measure**, paste one expression, and press Enter:

```DAX
Total Cases = COUNTROWS(Cases)
```

```DAX
Resolved Cases =
COUNTROWS(FILTER(Cases, NOT ISBLANK(Cases[resolved_at])))
```

```DAX
Open Backlog =
COUNTROWS(FILTER(Cases, ISBLANK(Cases[resolved_at])))
```

```DAX
Open Overdue =
VAR SnapshotTime = DATE(2025, 12, 31) + TIME(23, 59, 59)
RETURN
    COUNTROWS(
        FILTER(Cases, ISBLANK(Cases[resolved_at]) && Cases[due_at] < SnapshotTime)
    )
```

```DAX
Resolved SLA % =
DIVIDE(
    COUNTROWS(
        FILTER(Cases, NOT ISBLANK(Cases[resolved_at]) && Cases[resolved_at] <= Cases[due_at])
    ),
    [Resolved Cases]
)
```

```DAX
Average Resolution Hours =
AVERAGEX(
    FILTER(Cases, NOT ISBLANK(Cases[resolved_at])),
    (Cases[resolved_at] - Cases[created_at]) * 24
)
```

Format `Resolved SLA %` as a percentage with one decimal place and `Average Resolution Hours` as a decimal with one decimal place. These measures respect the report's filters. SLA compliance excludes open cases; overdue is a separate snapshot measure.

For monthly charts, add this calculated column using **New column**:

```DAX
Created Month = DATE(YEAR(Cases[created_at]), MONTH(Cases[created_at]), 1)
```

Set its format to `MMM yyyy` and use the column itself rather than the automatic date hierarchy on the chart axis.

## 3. Build the page

1. Add cards for `Total Cases`, `Resolved SLA %`, `Open Backlog`, `Open Overdue`, and `Average Resolution Hours`.
2. Add a clustered bar chart with `team` on the axis and `Resolved SLA %` as the value.
3. Add a column chart with `category` on the axis and `Open Overdue` as the value.
4. Add a line chart with `Created Month` on the axis and `Total Cases` as the value. Label it **Cases created by month**.
5. Add slicers for `team`, `category`, and `priority`. Add a title and a note stating that the data is synthetic and the snapshot is fixed.

The monthly chart shows creation volume, not historical backlog. Applying filters changes the population for the cards and charts.

## 4. Check and publish

1. Run `python scripts/run_analysis.py` as described in the README. With no slicers selected, compare the cards against the first SQL result. The SLA percentage should agree to one decimal place.
2. Explore the category and team results, then write down two or three observations supported by the displayed numbers. Treat these as patterns in simulated data, not evidence of real-world impact.
3. Save the report as `sla-backlog-dashboard.pbix`. Take a screenshot of the report.
4. On GitHub, open the repository and use **Add file > Upload files** to upload the `.pbix` and screenshot. Edit the README to describe your verified observations and link to the screenshot and report. Never upload real customer or confidential data.

Optionally publish the report to the Power BI service if you have the appropriate account and permissions. A public GitHub repository does not automatically host an interactive Power BI report; public web embedding has separate permissions and makes its data public.
