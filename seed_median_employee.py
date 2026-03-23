import argparse

from sqlalchemy import func, select, text

from database import create_tables, get_session
from models_median_employee import Employee

SEED_EMPLOYEES = [
    {"company": "A", "salary": 100},
    {"company": "A", "salary": 200},
    {"company": "A", "salary": 300},
    {"company": "B", "salary": 100},
    {"company": "B", "salary": 200},
    {"company": "B", "salary": 300},
    {"company": "B", "salary": 400},
    {"company": "C", "salary": 100},
    {"company": "C", "salary": 200},
    {"company": "C", "salary": 200},
    {"company": "C", "salary": 300},
    {"company": "D", "salary": 500},
]


def seed_employees(*, append: bool = False) -> int:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(text("TRUNCATE TABLE employees RESTART IDENTITY"))

        session.add_all(Employee(**row) for row in SEED_EMPLOYEES)
        session.commit()

        total_rows = session.scalar(select(func.count()).select_from(Employee))

    return total_rows or 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed test employee salary data.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    total_rows = seed_employees(append=args.append)
    mode = "appended" if args.append else "reset and seeded"
    print(
        f"Seed complete: {mode}. Inserted {len(SEED_EMPLOYEES)} rows; total rows now {total_rows}."
    )


if __name__ == "__main__":
    main()
