from sqlalchemy import and_, func, select, true
from sqlalchemy.orm import Session

from database import get_session

from .models import Employee, create_tables


def find_cumulative_salary(session: Session):

    all_ids = select(Employee.id).distinct().cte("all_ids")

    all_months = select(func.generate_series(1, 12).label("month")).cte("all_months")

    last_months = (
        select(Employee.id, func.max(Employee.month).label("last_month"))
        .group_by(Employee.id)
        .cte("last_months")
    )

    cumulative_salary = (
        select(
            all_ids.c.id,
            all_months.c.month,
            Employee.salary.label("salary"),
            func.sum(func.coalesce(Employee.salary, 0))
            .over(
                partition_by=all_ids.c.id,
                order_by=all_months.c.month,
                rows=(-2, 0),
            )
            .label("cumulative_salary"),
        )
        .select_from(all_ids.join(all_months, true()))
        .outerjoin(
            Employee,
            (Employee.id == all_ids.c.id) & (Employee.month == all_months.c.month),
        )
        .cte("cumulative_salary")
    )

    stmt = (
        select(
            cumulative_salary.c.id,
            cumulative_salary.c.month,
            cumulative_salary.c.cumulative_salary,
        )
        .join_from(
            cumulative_salary, last_months, (cumulative_salary.c.id == last_months.c.id)
        )
        .where(
            and_(
                cumulative_salary.c.salary.is_not(None),
                cumulative_salary.c.month != last_months.c.last_month,
            )
        )
        .order_by(cumulative_salary.c.id.asc(), cumulative_salary.c.month.desc())
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    with get_session() as session:
        rows = find_cumulative_salary(session)

    if not rows:
        print(
            "No rows found. Run `python -m problems.lc0579_find_cumulative_salary_of_an_employee.seed` first."
        )
        return

    for row in rows:
        print(
            f"id={row.id} month={row.month} cumulative_salary={row.cumulative_salary}"
        )


if __name__ == "__main__":
    main()
