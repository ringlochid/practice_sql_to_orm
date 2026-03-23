from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from database import get_session

from .models import Employee, Salary, create_tables


def get_average_salary_departments_vs_company(session: Session):
    average = (
        select(
            func.to_char(Salary.pay_date, "YYYY-MM").label("pay_month"),
            Employee.department_id,
            func.avg(Salary.amount)
            .over(partition_by=func.to_char(Salary.pay_date, "YYYY-MM"))
            .label("com_avg"),
            func.avg(Salary.amount)
            .over(
                partition_by=[
                    Employee.department_id,
                    func.to_char(Salary.pay_date, "YYYY-MM"),
                ],
            )
            .label("dep_avg"),
        )
        .join_from(Salary, Employee, Salary.employee_id == Employee.employee_id)
        .cte()
    )

    stmt = select(
        average.c.pay_month,
        average.c.department_id,
        case(
            (average.c.com_avg > average.c.dep_avg, "lower"),
            (average.c.com_avg < average.c.dep_avg, "higher"),
            else_="same",
        ).label("comparison"),
    ).group_by(
        average.c.pay_month,
        average.c.department_id,
        average.c.com_avg,
        average.c.dep_avg,
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    try:
        with get_session() as session:
            rows = get_average_salary_departments_vs_company(session)
    except NotImplementedError as exc:
        print(exc)
        return

    if not rows:
        print("No rows found.")
        return

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
