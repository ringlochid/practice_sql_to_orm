import argparse
from datetime import date

from sqlalchemy import func, select, text

from database import get_session

from .models import Employee, SCHEMA, Salary, create_tables

SEED_EMPLOYEES: list[dict[str, int]] = [
    {"employee_id": 1, "department_id": 1},
    {"employee_id": 2, "department_id": 2},
    {"employee_id": 3, "department_id": 2},
]

SEED_SALARIES: list[dict[str, int | date]] = [
    {"id": 1, "employee_id": 1, "amount": 9000, "pay_date": date(2017, 3, 31)},
    {"id": 2, "employee_id": 2, "amount": 6000, "pay_date": date(2017, 3, 31)},
    {"id": 3, "employee_id": 3, "amount": 10000, "pay_date": date(2017, 3, 31)},
    {"id": 4, "employee_id": 1, "amount": 7000, "pay_date": date(2017, 2, 28)},
    {"id": 5, "employee_id": 2, "amount": 6000, "pay_date": date(2017, 2, 28)},
    {"id": 6, "employee_id": 3, "amount": 8000, "pay_date": date(2017, 2, 28)},
]


def seed_average_salary(*, append: bool = False) -> tuple[int, int]:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(
                text(
                    f'TRUNCATE TABLE "{SCHEMA}".salaries, "{SCHEMA}".employees '
                    "RESTART IDENTITY CASCADE"
                )
            )

        if SEED_EMPLOYEES:
            session.add_all(Employee(**row) for row in SEED_EMPLOYEES)
            session.flush()

        if SEED_SALARIES:
            session.add_all(Salary(**row) for row in SEED_SALARIES)

        session.commit()

        total_employees = session.scalar(select(func.count()).select_from(Employee))
        total_salaries = session.scalar(select(func.count()).select_from(Salary))

    return (total_employees or 0, total_salaries or 0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold seed file for LC 615 Average Salary: Departments VS Company."
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    total_employees, total_salaries = seed_average_salary(append=args.append)
    mode = "appended" if args.append else "reset and seeded"
    print(
        "Seed complete: "
        f"{mode}. Totals now employees={total_employees}, salaries={total_salaries}."
    )


if __name__ == "__main__":
    main()
