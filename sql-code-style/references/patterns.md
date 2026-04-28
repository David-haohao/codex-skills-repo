# SQL Style Patterns (Business-Agnostic)

## 1) Layered Query Skeleton
```sql
WITH
base_keys AS (
    SELECT
        id,
        event_date,
        category
    FROM source_table
),
metric_block_a AS (
    SELECT
        id,
        event_date,
        COUNT(*) AS event_cnt
    FROM source_table
    GROUP BY id, event_date
),
metric_block_b AS (
    SELECT
        id,
        event_date,
        SUM(CASE WHEN status = 'ok' THEN amount ELSE 0 END) AS ok_amount
    FROM source_table
    GROUP BY id, event_date
)
SELECT
    k.id,
    k.event_date,
    k.category,
    COALESCE(a.event_cnt, 0) AS event_cnt,
    COALESCE(b.ok_amount, 0) AS ok_amount
FROM base_keys k
LEFT JOIN metric_block_a a
    ON k.id = a.id
   AND k.event_date = a.event_date
LEFT JOIN metric_block_b b
    ON k.id = b.id
   AND k.event_date = b.event_date;
```

## 2) Centralize Repeated Logic
Instead of repeating the same CASE logic in multiple metric blocks, define it once in an upstream layer and reuse the derived column.

## 3) Deviation Note Template
When deviating from preferred style, append a short note:
- Deviation: `<what changed>`
- Reason: `<why needed>`
- Impact: `<readability/perf/portability tradeoff>`

## 4) Dialect Isolation Pattern
Keep the core query ANSI-first. If dialect-specific syntax is required, isolate it in one layer and annotate it briefly.

