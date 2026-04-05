WITH all_ids AS (
    SELECT
        DISTINCT id
    FROM
        Employee
),
all_months AS (
    SELECT
        generate_series(1, 12) AS month
),
last_months AS (
    SELECT
        id,
        MAX(month) AS max_month
    FROM
        Employee
    GROUP BY
        id
),
cumulative_salaries AS (
    SELECT
        ai.id,
        am.month,
        e.salary,
        SUM(COALESCE(e.salary, 0)) OVER(
            PARTITION BY ai.id
            ORDER BY
                am.month ROWS BETWEEN 2 PRECEDING
                AND CURRENT ROW
        ) AS cumulative_salary
    FROM
        all_ids ai
        CROSS JOIN all_months am
        LEFT JOIN Employee e ON ai.id = e.id
        AND am.month = e.month
)
SELECT
    cs.id,
    cs.month,
    cs.cumulative_salary AS Salary
FROM
    cumulative_salaries cs
    JOIN last_months lm ON cs.id = lm.id
WHERE
    cs.salary IS NOT NULL
    AND cs.month <> lm.max_month
ORDER BY
    cs.id ASC,
    cs.month DESC