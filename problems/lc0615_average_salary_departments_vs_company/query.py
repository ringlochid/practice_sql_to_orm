from sqlalchemy.orm import Session

from database import get_session

from .models import create_tables


def get_average_salary_departments_vs_company(session: Session):
    raise NotImplementedError("TODO: implement the LC 615 ORM query here.")


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
