from datetime import date

from sqlalchemy import DECIMAL, and_, case, func, select
from sqlalchemy.orm import Session, aliased

from database import get_session

from .models import StatusType, Trip, User, create_tables


def get_cancellation_rate(session: Session):

    client = aliased(User)
    driver = aliased(User)

    valid_trips = (
        select(
            Trip.id,
            Trip.status,
            Trip.request_at,
        )
        .select_from(Trip)
        .join(client, and_(Trip.client_id == client.id, client.banned.is_(False)))
        .join(driver, and_(Trip.driver_id == driver.id, driver.banned.is_(False)))
        .where(
            and_(
                Trip.request_at >= date(2013, 10, 1),
                Trip.request_at <= date(2013, 10, 3),
            )
        )
        .cte("valid_trips")
    )

    aggregation = (
        select(
            valid_trips.c.request_at.label("Day"),
            func.sum(
                case((valid_trips.c.status != StatusType.COMPLETED, 1), else_=0)
            ).label("CanceledTrips"),
            func.count(valid_trips.c.id).label("TotalTrips"),
        )
        .select_from(valid_trips)
        .group_by(valid_trips.c.request_at)
        .cte("aggregation")
    )

    stmt = select(
        aggregation.c.Day,
        func.round(
            func.cast(aggregation.c.CanceledTrips, DECIMAL(10, 2))
            / aggregation.c.TotalTrips,
            2,
        ).label("CancellationRate"),
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    with get_session() as session:
        rows = get_cancellation_rate(session)

    if not rows:
        print(
            "No rows found. Run `python -m problems.lc0262_trips_and_users.seed` first."
        )
        return

    for row in rows:
        print(f"Day={row.Day} CancellationRate={row.CancellationRate}")


if __name__ == "__main__":
    main()
