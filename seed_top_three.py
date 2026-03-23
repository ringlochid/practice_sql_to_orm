import argparse

from sqlalchemy import func, select, text

from database import create_tables, get_session
from models_top_three import Department, Employee

SEED_DEPARTMENTS = [
    {"name": "IT"},
    {"name": "Sales"},
]

SEED_EMPLOYEES = [
    {"name": "Joe", "salary": 85000, "department": "IT"},
    {"name": "Henry", "salary": 80000, "department": "Sales"},
    {"name": "Sam", "salary": 60000, "department": "Sales"},
    {"name": "Max", "salary": 90000, "department": "IT"},
    {"name": "Janet", "salary": 69000, "department": "IT"},
    {"name": "Randy", "salary": 85000, "department": "IT"},
    {"name": "Will", "salary": 70000, "department": "IT"},
    {"name": "Jane", "salary": 60000, "department": "IT"},
    {"name": "Zhang", "salary": 50000, "department": "IT"},
    {"name": "Leo", "salary": 40000, "department": "IT"},
    {"name": "Lochid", "salary": 140000, "department": "IT"},
]


def seed_top_three(*, append: bool = False) -> tuple[int, int]:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(
                text('TRUNCATE TABLE "Employee", "Department" RESTART IDENTITY CASCADE')
            )

        departments_by_name: dict[str, Department] = {
            department.name: department
            for department in session.scalars(select(Department)).all()
        }

        for row in SEED_DEPARTMENTS:
            if row["name"] not in departments_by_name:
                department = Department(name=row["name"])
                session.add(department)
                session.flush()
                departments_by_name[row["name"]] = department

        session.add_all(
            Employee(
                name=row["name"],
                salary=row["salary"],
                departmentId=departments_by_name[row["department"]].id,
            )
            for row in SEED_EMPLOYEES
        )
        session.commit()

        total_departments = session.scalar(select(func.count()).select_from(Department))
        total_employees = session.scalar(select(func.count()).select_from(Employee))

    return (total_departments or 0, total_employees or 0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed Department Top Three Salaries example data."
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    total_departments, total_employees = seed_top_three(append=args.append)
    mode = "appended" if args.append else "reset and seeded"
    print(
        "Seed complete: "
        f"{mode}. Inserted {len(SEED_DEPARTMENTS)} departments and {len(SEED_EMPLOYEES)} employees; "
        f"totals now departments={total_departments}, employees={total_employees}."
    )


if __name__ == "__main__":
    main()
