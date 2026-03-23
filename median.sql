WITH ranked AS (
  SELECT
    e.id,
    e.company,
    e.salary,
    ROW_NUMBER() OVER (
      PARTITION BY e.company
      ORDER BY e.salary, e.id
    ) AS salary_rownum
  FROM employees e
),
company_stats AS (
  SELECT
    company,
    (COUNT(*) + 1) / 2 AS lower_row,
    (COUNT(*) + 2) / 2 AS upper_row
  FROM employees
  GROUP BY company
)
SELECT r.id, r.company, r.salary
FROM ranked r
JOIN company_stats s
  ON s.company = r.company
WHERE r.salary_rownum >= s.lower_row
  AND r.salary_rownum <= s.upper_row
ORDER BY r.company, r.salary, r.id;
