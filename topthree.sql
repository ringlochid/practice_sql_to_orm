WITH ranked_employee AS (
    SELECT *, DENSE_RANK()OVER(PARTITION BY departmentId ORDER BY salary DESC) AS rank
    FROM Employee
)
SELECT d.name AS Department, re.name AS Employee, re.salary AS Salary
FROM ranked_employee re
JOIN Department d ON re.departmentId = d.id
WHERE re.rank <= 3