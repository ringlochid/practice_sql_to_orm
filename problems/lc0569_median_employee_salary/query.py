from sqlalchemy import Integer, cast, func, select
from sqlalchemy.orm import Session

from database import get_session

from .models import Employee, create_tables


def get_median_salary_per_company(session: Session):
    ranked_employees = select(
        Employee.id.label("id"),
        Employee.company.label("company"),
        Employee.salary.label("salary"),
        func.row_number()
        .over(
            partition_by=Employee.company,
            order_by=(Employee.salary, Employee.id),
        )
        .label("salary_rownum"),
    ).cte("ranked_employees")

    company_stats = (
        select(
            Employee.company.label("company"),
            cast(func.floor((func.count() + 1) / 2), Integer).label("lower_row"),
            cast(func.floor((func.count() + 2) / 2), Integer).label("upper_row"),
        )
        .group_by(Employee.company)
        .cte("company_stats")
    )

    stmt = (
        select(
            ranked_employees.c.id,
            ranked_employees.c.company,
            ranked_employees.c.salary,
        )
        .join(company_stats, company_stats.c.company == ranked_employees.c.company)
        .where(ranked_employees.c.salary_rownum >= company_stats.c.lower_row)
        .where(ranked_employees.c.salary_rownum <= company_stats.c.upper_row)
        .order_by(
            ranked_employees.c.company,
            ranked_employees.c.salary,
            ranked_employees.c.id,
        )
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    with get_session() as session:
        rows = get_median_salary_per_company(session)

    if not rows:
        print("No rows found. Run `python -m problems.lc0569_median_employee_salary.seed` first.")
        return

    for row in rows:
        print(f"id={row.id} company={row.company} salary={row.salary}")


if __name__ == "__main__":
    main()
