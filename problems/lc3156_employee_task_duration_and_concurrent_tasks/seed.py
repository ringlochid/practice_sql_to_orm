import argparse
from datetime import datetime

from sqlalchemy import func, select, text

from database import get_session

from .models import SCHEMA, Task, create_tables

SEED_TASKS: list[dict[str, int | datetime]] = [
    {
        "task_id": 1,
        "employee_id": 1001,
        "start_time": datetime(2023, 5, 1, 8, 0, 0),
        "end_time": datetime(2023, 5, 1, 9, 0, 0),
    },
    {
        "task_id": 2,
        "employee_id": 1001,
        "start_time": datetime(2023, 5, 1, 8, 30, 0),
        "end_time": datetime(2023, 5, 1, 10, 30, 0),
    },
    {
        "task_id": 3,
        "employee_id": 1001,
        "start_time": datetime(2023, 5, 1, 11, 0, 0),
        "end_time": datetime(2023, 5, 1, 12, 0, 0),
    },
    {
        "task_id": 7,
        "employee_id": 1001,
        "start_time": datetime(2023, 5, 1, 13, 0, 0),
        "end_time": datetime(2023, 5, 1, 15, 30, 0),
    },
    {
        "task_id": 4,
        "employee_id": 1002,
        "start_time": datetime(2023, 5, 1, 9, 0, 0),
        "end_time": datetime(2023, 5, 1, 10, 0, 0),
    },
    {
        "task_id": 5,
        "employee_id": 1002,
        "start_time": datetime(2023, 5, 1, 9, 30, 0),
        "end_time": datetime(2023, 5, 1, 11, 30, 0),
    },
    {
        "task_id": 6,
        "employee_id": 1003,
        "start_time": datetime(2023, 5, 1, 14, 0, 0),
        "end_time": datetime(2023, 5, 1, 16, 0, 0),
    },
]


def seed_tasks(*, append: bool = False) -> int:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(text(f'TRUNCATE TABLE "{SCHEMA}".tasks RESTART IDENTITY'))

        session.add_all(Task(**row) for row in SEED_TASKS)
        session.commit()

        total_rows = session.scalar(select(func.count()).select_from(Task))

    return total_rows or 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed LC 3156 Employee Task Duration and Concurrent Tasks data."
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    total_rows = seed_tasks(append=args.append)
    mode = "appended" if args.append else "reset and seeded"
    print(
        f"Seed complete: {mode}. Inserted {len(SEED_TASKS)} rows; total rows now {total_rows}."
    )


if __name__ == "__main__":
    main()
