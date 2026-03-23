from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from database import create_tables, get_session
from models_top_three import Department, Employee


def get_top_three(session: Session):
    ranked_employee = select(
        Employee.id,
        Employee.name,
        Employee.salary,
        Employee.departmentId,
        func.dense_rank()
        .over(
            partition_by=Employee.departmentId,
            order_by=desc(Employee.salary),
        )
        .label("rank"),
    ).cte("ranked_employee")

    stmt = (
        select(
            Department.name.label("Department"),
            ranked_employee.c.name.label("Employee"),
            ranked_employee.c.salary.label("Salary"),
        )
        .join_from(
            ranked_employee, Department, ranked_employee.c.departmentId == Department.id
        )
        .where(ranked_employee.c.rank <= 3)
        .order_by(Department.name, desc(ranked_employee.c.salary), ranked_employee.c.name)
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    with get_session() as session:
        rows = get_top_three(session)

    if not rows:
        print("No rows found. Run seed_top_three.py first.")
        return

    for row in rows:
        print(
            f"Department={row.Department} Employee={row.Employee} Salary={row.Salary}"
        )


if __name__ == "__main__":
    main()
