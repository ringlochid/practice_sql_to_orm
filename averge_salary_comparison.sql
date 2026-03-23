-- Write your PostgreSQL query statement below

WITH company_avg AS (
    SELECT TO_CHAR(pay_date, 'YYYY-MM') AS pay_month, AVG(amount) AS avg_salary
    FROM Salary
    GROUP BY TO_CHAR(pay_date, 'YYYY-MM')
),
dep_avg AS (
    SELECT e.department_id, TO_CHAR(pay_date, 'YYYY-MM') AS pay_month, AVG(amount) AS avg_salary
    FROM Salary s
    JOIN Employee e
    ON s.employee_id = e.employee_id
    GROUP BY e.department_id, TO_CHAR(pay_date, 'YYYY-MM')
)
SELECT c.pay_month, d.department_id,
    CASE
        WHEN d.avg_salary > c.avg_salary THEN 'higher'
        WHEN d.avg_salary < c.avg_salary THEN 'lower'
        ELSE 'same'
    END
    AS comparison
FROM company_avg c
JOIN dep_avg d
ON c.pay_month = d.pay_month