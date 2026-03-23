WITH ranked_employees AS (
    SELECT
        e.id,
        e.company,
        e.salary,
        ROW_NUMBER() OVER (
            PARTITION BY e.company
            ORDER BY e.salary, e.id
        ) AS salary_rownum
    FROM lc0569_median_employee_salary.employees AS e
),
company_stats AS (
    SELECT
        company,
        (COUNT(*) + 1) / 2 AS lower_row,
        (COUNT(*) + 2) / 2 AS upper_row
    FROM lc0569_median_employee_salary.employees
    GROUP BY company
)
SELECT re.id, re.company, re.salary
FROM ranked_employees AS re
JOIN company_stats AS cs
    ON cs.company = re.company
WHERE re.salary_rownum >= cs.lower_row
  AND re.salary_rownum <= cs.upper_row
ORDER BY re.company, re.salary, re.id;
