WITH ranked_employees AS (
    SELECT
        e.id,
        e.name,
        e.salary,
        e.department_id,
        DENSE_RANK() OVER (
            PARTITION BY e.department_id
            ORDER BY
                e.salary DESC
        ) AS salary_rank
    FROM
        lc0185_department_top_three_salaries.employees AS e
)
SELECT
    d.name AS "Department",
    re.name AS "Employee",
    re.salary AS "Salary"
FROM
    ranked_employees AS re
    JOIN lc0185_department_top_three_salaries.departments AS d ON d.id = re.department_id
WHERE
    re.salary_rank <= 3
ORDER BY
    d.name,
    re.salary DESC,
    re.name;