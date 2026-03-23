# SQLAlchemy ORM Problem Layout

This repo now keeps each practice problem in its own package under `problems/`.
Shared database setup stays in `database.py`; each problem package owns its own SQLAlchemy `Base`, Postgres `SCHEMA`, models, seed data, and `create_tables()`.

## Structure

```text
problems/
  lc0569_median_employee_salary/
  lc0185_department_top_three_salaries/
  lc0615_average_salary_departments_vs_company/
  lc1892_page_recommendations_ii/
```

Each package contains:

- `models.py`: local schema, ORM models, and `create_tables()`
- `seed.py`: sample data loader with `--append`
- `query.py`: ORM solution runnable with `python -m`
- `query.sql`: raw SQL solution against the same schema

## Run

Start Postgres:

```bash
docker compose up -d --wait
```

Run the Python modules with the project virtualenv, or activate it first and use `python -m ...`.

Median Employee Salary:

```bash
./.venv/bin/python -m problems.lc0569_median_employee_salary.seed
./.venv/bin/python -m problems.lc0569_median_employee_salary.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc0569_median_employee_salary/query.sql
```

Department Top Three Salaries:

```bash
./.venv/bin/python -m problems.lc0185_department_top_three_salaries.seed
./.venv/bin/python -m problems.lc0185_department_top_three_salaries.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc0185_department_top_three_salaries/query.sql
```

Average Salary: Departments VS Company (scaffold only for now):

```bash
./.venv/bin/python -m problems.lc0615_average_salary_departments_vs_company.seed
./.venv/bin/python -m problems.lc0615_average_salary_departments_vs_company.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc0615_average_salary_departments_vs_company/query.sql
```

Page Recommendations II:

```bash
./.venv/bin/python -m problems.lc1892_page_recommendations_ii.seed
./.venv/bin/python -m problems.lc1892_page_recommendations_ii.query
docker compose exec -T postgres psql -U postgres -d orm_practice < problems/lc1892_page_recommendations_ii/query.sql
```
