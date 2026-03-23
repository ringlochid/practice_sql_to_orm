from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from database import get_session

from .models import Department, Employee, create_tables


def get_department_top_three_salaries(session: Session):
    ranked_employees = select(
        Employee.id,
        Employee.name,
        Employee.salary,
        Employee.department_id,
        func.dense_rank()
        .over(
            partition_by=Employee.department_id,
            order_by=desc(Employee.salary),
        )
        .label("salary_rank"),
    ).cte("ranked_employees")

    stmt = (
        select(
            Department.name.label("Department"),
            ranked_employees.c.name.label("Employee"),
            ranked_employees.c.salary.label("Salary"),
        )
        .join_from(
            ranked_employees,
            Department,
            ranked_employees.c.department_id == Department.id,
        )
        .where(ranked_employees.c.salary_rank <= 3)
        .order_by(
            Department.name,
            desc(ranked_employees.c.salary),
            ranked_employees.c.name,
        )
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    with get_session() as session:
        rows = get_department_top_three_salaries(session)

    if not rows:
        print(
            "No rows found. Run `python -m problems.lc0185_department_top_three_salaries.seed` first."
        )
        return

    for row in rows:
        print(
            f"Department={row.Department} Employee={row.Employee} Salary={row.Salary}"
        )


if __name__ == "__main__":
    main()
