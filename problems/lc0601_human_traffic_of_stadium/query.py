from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_session

from .models import Stadium, create_tables


def get_human_traffic_of_stadium(session: Session):
    grouped_rows = (
        select(
            Stadium.id,
            Stadium.visit_date,
            Stadium.people,
            (
                Stadium.id - func.row_number().over(order_by=Stadium.id)
            ).label("group_id"),
        )
        .where(Stadium.people >= 100)
        .cte("grouped_rows")
    )

    valid_groups = (
        select(grouped_rows.c.group_id)
        .group_by(grouped_rows.c.group_id)
        .having(func.count() >= 3)
    ).cte("valid_groups")

    stmt = (
        select(Stadium)
        .join(grouped_rows, Stadium.id == grouped_rows.c.id)
        .where(grouped_rows.c.group_id.in_(select(valid_groups.c.group_id)))
        .order_by(Stadium.visit_date)
    )

    return session.execute(stmt).scalars().all()


def main():
    create_tables()

    with get_session() as session:
        rows = get_human_traffic_of_stadium(session)

    if not rows:
        print(
            "No rows found. Run `python -m problems.lc0601_human_traffic_of_stadium.seed` first."
        )
        return

    for row in rows:
        print(f"ID={row.id}, Date={row.visit_date}, People={row.people}")

    pass


if __name__ == "__main__":
    main()
