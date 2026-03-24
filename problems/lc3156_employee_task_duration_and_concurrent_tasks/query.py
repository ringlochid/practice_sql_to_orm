from sqlalchemy.orm import Session

from database import get_session

from .models import create_tables


def get_employee_task_duration_and_concurrent_tasks(session: Session):
    raise NotImplementedError("TODO: implement the LC 3156 ORM query here.")


def main() -> None:
    create_tables()

    try:
        with get_session() as session:
            rows = get_employee_task_duration_and_concurrent_tasks(session)
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
