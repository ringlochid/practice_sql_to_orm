import argparse

from sqlalchemy import func, select, text

from database import get_session

from .models import SCHEMA, Employee, create_tables

SEED_EMPLOYEES: list[dict[str, int]] = [
    {"id": 1, "month": 1, "salary": 20},
    {"id": 2, "month": 1, "salary": 20},
    {"id": 1, "month": 2, "salary": 30},
    {"id": 2, "month": 2, "salary": 30},
    {"id": 3, "month": 2, "salary": 40},
    {"id": 1, "month": 3, "salary": 40},
    {"id": 3, "month": 3, "salary": 60},
    {"id": 1, "month": 4, "salary": 60},
    {"id": 3, "month": 4, "salary": 70},
    {"id": 1, "month": 7, "salary": 90},
    {"id": 1, "month": 8, "salary": 90},
]


def seed_employees(*, append: bool = False) -> tuple[int, int]:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(
                text(f'TRUNCATE TABLE "{SCHEMA}".employees RESTART IDENTITY CASCADE')
            )
            rows_to_insert = SEED_EMPLOYEES
        else:
            existing_keys = set(
                session.execute(select(Employee.id, Employee.month)).all()
            )
            rows_to_insert = [
                row
                for row in SEED_EMPLOYEES
                if (row["id"], row["month"]) not in existing_keys
            ]

        if rows_to_insert:
            session.add_all(Employee(**row) for row in rows_to_insert)

        session.commit()

        inserted = len(rows_to_insert)
        total_rows = session.scalar(select(func.count()).select_from(Employee)) or 0

    return inserted, total_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Employee data.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append only missing seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    inserted, total_rows = seed_employees(append=args.append)
    mode = "appended" if args.append else "reset and seeded"
    print(
        "Seed complete: "
        f"{mode}. Inserted {inserted} employee rows; totals now employee={total_rows}."
    )


if __name__ == "__main__":
    main()
