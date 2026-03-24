# SQL → SQLAlchemy ORM practice repo

This repo is for **translating LeetCode-style SQL problems into SQLAlchemy ORM** in a way that is easy to rerun, compare, and extend.

The goal is not just to get one answer working.
The goal is to build a **repeatable pattern**:

1. define the problem tables locally
2. seed the sample data
3. write or keep the raw SQL version
4. translate it into SQLAlchemy ORM
5. compare outputs until both agree

---

## What the structure is doing

Each problem lives in its own package under `problems/`.

```text
problems/
  lc0569_median_employee_salary/
  lc0185_department_top_three_salaries/
  lc0615_average_salary_departments_vs_company/
  lc1892_page_recommendations_ii/
  lc3156_employee_task_duration_and_concurrent_tasks/
```

Each package contains:

- `models.py` → local SQLAlchemy models for that problem
- `seed.py` → sample data loader for local testing
- `query.py` → ORM solution
- `query.sql` → raw SQL version
- `__init__.py` → package marker

The shared root `database.py` only provides:

- `engine`
- `SessionLocal`
- `get_session()`

It does **not** know about any specific problem.
Each problem owns its own `Base`, `SCHEMA`, and `create_tables()`.

---

## Why use PostgreSQL schemas

All problems use the same database: `orm_practice`.

They are separated by **schema**, not by separate databases.
That means you can safely reuse generic table names like `employees`, `departments`, `salaries`, `likes`, etc. without collisions.

Examples:

- `lc0569_median_employee_salary.employees`
- `lc0185_department_top_three_salaries.employees`
- `lc0615_average_salary_departments_vs_company.salaries`

This keeps the repo simple:

- one Docker Postgres container
- one database
- many isolated problem namespaces

---

## Important run rule

Run problem files as **modules from the repo root**.

### Correct

```bash
cd ~/leo/practice/orm/sqlalchemy_p
./.venv/bin/python -m problems.lc0185_department_top_three_salaries.seed
./.venv/bin/python -m problems.lc0185_department_top_three_salaries.query
```

### Wrong

```bash
cd problems/lc0185_department_top_three_salaries
python seed.py
```

Why: these folders are Python packages. Running from inside the folder breaks import resolution for `database.py` and sibling package modules.

---

## Quick start

Start Postgres:

```bash
docker compose up -d --wait
```

Then run a problem from the repo root.

### LC 569 — Median Employee Salary

```bash
./.venv/bin/python -m problems.lc0569_median_employee_salary.seed
./.venv/bin/python -m problems.lc0569_median_employee_salary.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc0569_median_employee_salary/query.sql
```

### LC 185 — Department Top Three Salaries

```bash
./.venv/bin/python -m problems.lc0185_department_top_three_salaries.seed
./.venv/bin/python -m problems.lc0185_department_top_three_salaries.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc0185_department_top_three_salaries/query.sql
```

### LC 615 — Average Salary: Departments VS Company

```bash
./.venv/bin/python -m problems.lc0615_average_salary_departments_vs_company.seed
./.venv/bin/python -m problems.lc0615_average_salary_departments_vs_company.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc0615_average_salary_departments_vs_company/query.sql
```

Note: LC 615 is currently a **scaffold only**. The folder exists, but the ORM solution is intentionally left blank.

### LC 1892 — Page Recommendations II

```bash
./.venv/bin/python -m problems.lc1892_page_recommendations_ii.seed
./.venv/bin/python -m problems.lc1892_page_recommendations_ii.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc1892_page_recommendations_ii/query.sql
```

### LC 3156 — Employee Task Duration and Concurrent Tasks

```bash
./.venv/bin/python -m problems.lc3156_employee_task_duration_and_concurrent_tasks.seed
./.venv/bin/python -m problems.lc3156_employee_task_duration_and_concurrent_tasks.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc3156_employee_task_duration_and_concurrent_tasks/query.sql
```

Note: LC 3156 is currently scaffolded with sample seed data, but the ORM and raw SQL solution files are left as TODO placeholders.

---

## The workflow for a new problem

When adding a new SQL problem, follow this pattern.

### 1. Create a package

Example:

```text
problems/lc1234_problem_slug/
  __init__.py
  models.py
  seed.py
  query.py
  query.sql
```

Use a stable name:

```text
lc<leetcode_number>_<problem_slug>
```

Example:

- `lc0185_department_top_three_salaries`
- `lc1892_page_recommendations_ii`

### 2. Define the models in `models.py`

Each problem should have:

- `SCHEMA = "lc1234_problem_slug"`
- its own `Base`
- ORM models for the problem tables
- `create_tables()` that creates the schema and then calls `Base.metadata.create_all(...)`

This makes every problem self-contained.

### 3. Put sample data in `seed.py`

The seed file is there to make the problem easy to rerun.

Use it for:

- LeetCode sample input
- extra local test cases if you want them
- reset/append behavior for fast iteration

### 4. Write the raw SQL in `query.sql`

Keep the raw SQL version in the same package.
That gives you a stable reference for what the ORM query is supposed to do.

### 5. Translate the SQL into SQLAlchemy ORM in `query.py`

This is the actual practice step.
The ORM version should aim to match the SQL result shape as closely as possible.

### 6. Compare the results

Run:

- seed
- ORM query
- raw SQL

If the outputs disagree, the bug is somewhere in your translation, seed data, or schema shape.

---

## Practical translation checklist

When translating SQL to SQLAlchemy ORM, this is the pattern to think in.

### SQL building blocks → SQLAlchemy equivalents

- `SELECT ...` → `select(...)`
- `WHERE ...` → `.where(...)`
- `JOIN ...` → `.join(...)` or `.join_from(...)`
- `LEFT JOIN ...` → `.outerjoin(...)`
- `GROUP BY ...` → `.group_by(...)`
- `HAVING ...` → `.having(...)`
- `ORDER BY ...` → `.order_by(...)`
- `DISTINCT` → `.distinct()`
- `COUNT / SUM / AVG / MIN / MAX` → `func.count`, `func.sum`, `func.avg`, ...
- `COUNT(DISTINCT x)` → `func.count(distinct(x))`
- `AS alias` → `.label("alias")`
- `UNION` → `union(...)`
- `UNION ALL` → `union_all(...)`
- `INTERSECT` → `intersect(...)`
- `EXCEPT` → `except_(...)`
- `CASE WHEN ... THEN ... ELSE ... END` → `case((cond, value), ..., else_=...)`
- `CAST(x AS type)` → `cast(x, SomeType)`
- `COALESCE(...)` → `func.coalesce(...)`
- `IN (...)` → `.in_(...)`
- `BETWEEN a AND b` → `.between(a, b)`
- `LIKE / ILIKE` → `.like(...)`, `.ilike(...)`
- `EXISTS (...)` → `select(...).where(...).exists()`
- `NOT EXISTS (...)` → `~select(...).where(...).exists()`
- `CTE` → `.cte("name")`
- subquery → `.subquery()`
- window function → `func.row_number().over(...)`, `func.dense_rank().over(...)`, `func.lead(...).over(...)`, `func.lag(...).over(...)`
- descending sort → `desc(column)`
- tuple comparisons → `tuple_(...)`

### Common mental translation patterns

#### A. Aggregate report

SQL shape:

```sql
SELECT x, COUNT(*)
FROM table
GROUP BY x
```

ORM shape:

```python
select(table.c.x, func.count()).group_by(table.c.x)
```

#### B. Window ranking

SQL shape:

```sql
DENSE_RANK() OVER (PARTITION BY ... ORDER BY ...)
```

ORM shape:

```python
func.dense_rank().over(partition_by=..., order_by=...)
```

#### C. CTE-based step-by-step query

SQL shape:

```sql
WITH a AS (...), b AS (...)
SELECT ...
```

ORM shape:

```python
a = select(...).cte("a")
b = select(...).cte("b")
stmt = select(...)
```

#### D. Exclude rows already owned/liked/seen

SQL shape:

```sql
WHERE (x, y) NOT IN (SELECT ...)
```

ORM shape:

```python
.where(~tuple_(x, y).in_(subquery.select()))
```

If `NOT IN` starts behaving weirdly with `NULL`s, rewrite it as `NOT EXISTS` or use an anti-join.

#### E. Set operations

SQL shape:

```sql
SELECT ... FROM a
UNION ALL
SELECT ... FROM b
```

ORM shape:

```python
combined = union_all(select(...), select(...)).cte("combined")
stmt = select(combined.c.some_col)
```

Same idea for:

- `union(...)`
- `intersect(...)`
- `except_(...)`

A very SQLAlchemy-ish move is to wrap the set operation in a `cte(...)` or `subquery()` before doing more filtering, grouping, or ordering.

#### F. Anti-join / NOT EXISTS

SQL shape:

```sql
WHERE NOT EXISTS (
    SELECT 1
    FROM other
    WHERE other.x = main.x
)
```

ORM shape:

```python
subq = select(1).where(other.c.x == main.c.x)
stmt = select(main.c.x).where(~subq.exists())
```

This is often cleaner and safer than `NOT IN`, especially if `NULL`s are involved.

#### G. Self-join with aliases

SQL shape:

```sql
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.id
```

ORM shape:

```python
from sqlalchemy.orm import aliased

e1 = aliased(Employee)
e2 = aliased(Employee)

stmt = select(e1.name, e2.name).join(e2, e1.manager_id == e2.id)
```

Use `aliased(...)` whenever the same model appears more than once in a query.

#### H. Conditional aggregate

SQL shape:

```sql
SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END)
```

ORM shape:

```python
func.sum(case((table.c.status == "done", 1), else_=0))
```

This shows up all the time in report-style problems.

#### I. Window first, collapse later

SQL shape:

```sql
WITH ranked AS (... window function ...)
SELECT ...
FROM ranked
WHERE ...
```

ORM shape:

```python
ranked = select(..., func.row_number().over(...).label("rn")).cte("ranked")
stmt = select(ranked.c.some_col).where(ranked.c.rn == 1)
```

This is one of the most useful SQLAlchemy habits: compute the window columns in one step, then do filtering/grouping in an outer step.

### More SQLAlchemy-ish habits

These are not direct SQL translations, but they tend to make ORM query code much cleaner.

- **Name your intermediate steps**: `base`, `ranked`, `monthly`, `deduped`, `final`
- **Use `.cte(...)` when the SQL naturally has `WITH` blocks**
- **Use `.subquery()` for inline derived tables; use `.cte()` when readability matters more**
- **Prefer explicit `.join_from(left, right, onclause)` when the join path is not obvious**
- **Label computed columns early** with `.label(...)` so outer queries are easier to read
- **After window functions, return to an outer `select(...)`** instead of cramming everything into one statement
- **After `union_all(...)` / `intersect(...)` / `except_(...)`, wrap the result** before applying final filters or ordering
- **Use `.c.column_name` consistently** when selecting from a CTE or subquery
- **Keep the ORM query shaped like the SQL logic**, not like a random chain of method calls
- **Debug by matching stages**: seed output → raw SQL output → ORM output

---

## What to focus on while practicing

The point is not memorizing SQLAlchemy syntax blindly.
Focus on identifying the **query pattern** first:

- plain join
- aggregate per group
- top-N per group
- median / rank / nth row
- anti-join / exclusion
- self-join or bidirectional relationship
- window function
- nested CTE pipeline

Once you know the pattern, the ORM translation gets much easier.

That is the real practice loop in this repo:

**SQL pattern → intermediate result shape → ORM translation**

---

## Suggested way to work on a problem

1. Read the problem and sample tables.
2. Create or check `models.py`.
3. Put the sample rows into `seed.py`.
4. Write `query.sql` first if the SQL logic is still fuzzy.
5. Translate it into `query.py`.
6. Run both versions.
7. Compare row count, row values, and ordering.
8. Clean up names only after the logic is correct.

That order tends to be faster than trying to freestyle SQLAlchemy from scratch.

---

## Current repo conventions

- package name format: `lcXXXX_problem_slug`
- one package per problem
- one local Postgres schema per problem
- shared DB session infra in root `database.py`
- run everything from the repo root with `python -m`
- keep raw SQL beside the ORM version
- prefer clarity over clever abstractions

---

## If you are adding another problem

Copy an existing folder that is structurally similar.

Good references:

- use `lc0569_median_employee_salary` for window/row-number style work
- use `lc0185_department_top_three_salaries` for dense-rank per group
- use `lc1892_page_recommendations_ii` for CTE + union + exclusion patterns

If the new problem is only scaffolded, it is okay for `query.py` to raise a friendly TODO first.
That is still useful structure.

---

## Final idea

This repo is basically a **pattern translation lab**.

Each folder is one isolated exercise in turning:

- table definitions
- sample data
- SQL logic

into a working SQLAlchemy ORM query that you can rerun anytime.

That is the whole game.
