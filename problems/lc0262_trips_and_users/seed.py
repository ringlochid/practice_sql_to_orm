import argparse
from datetime import date

from sqlalchemy import func, select, text

from database import get_session

from .models import SCHEMA, StatusType, Trip, User, UserType, create_tables

SEED_USERS: list[dict[str, int | bool | UserType]] = [
    {"id": 1, "banned": False, "role": UserType.CLIENT},
    {"id": 2, "banned": True, "role": UserType.CLIENT},
    {"id": 3, "banned": False, "role": UserType.CLIENT},
    {"id": 4, "banned": False, "role": UserType.CLIENT},
    {"id": 10, "banned": False, "role": UserType.DRIVER},
    {"id": 11, "banned": False, "role": UserType.DRIVER},
    {"id": 12, "banned": False, "role": UserType.DRIVER},
    {"id": 13, "banned": False, "role": UserType.DRIVER},
]

SEED_TRIPS: list[dict[str, int | StatusType | date]] = [
    {
        "id": 1,
        "client_id": 1,
        "driver_id": 10,
        "city_id": 1,
        "status": StatusType.COMPLETED,
        "request_at": date(2013, 10, 1),
    },
    {
        "id": 2,
        "client_id": 2,
        "driver_id": 11,
        "city_id": 1,
        "status": StatusType.CANCELED_BY_DRIVER,
        "request_at": date(2013, 10, 1),
    },
    {
        "id": 3,
        "client_id": 3,
        "driver_id": 12,
        "city_id": 6,
        "status": StatusType.COMPLETED,
        "request_at": date(2013, 10, 1),
    },
    {
        "id": 4,
        "client_id": 4,
        "driver_id": 13,
        "city_id": 6,
        "status": StatusType.CANCELED_BY_CLIENT,
        "request_at": date(2013, 10, 1),
    },
    {
        "id": 5,
        "client_id": 1,
        "driver_id": 10,
        "city_id": 1,
        "status": StatusType.COMPLETED,
        "request_at": date(2013, 10, 2),
    },
    {
        "id": 6,
        "client_id": 2,
        "driver_id": 11,
        "city_id": 6,
        "status": StatusType.COMPLETED,
        "request_at": date(2013, 10, 2),
    },
    {
        "id": 7,
        "client_id": 3,
        "driver_id": 12,
        "city_id": 6,
        "status": StatusType.COMPLETED,
        "request_at": date(2013, 10, 2),
    },
    {
        "id": 8,
        "client_id": 2,
        "driver_id": 12,
        "city_id": 12,
        "status": StatusType.COMPLETED,
        "request_at": date(2013, 10, 3),
    },
    {
        "id": 9,
        "client_id": 3,
        "driver_id": 10,
        "city_id": 12,
        "status": StatusType.COMPLETED,
        "request_at": date(2013, 10, 3),
    },
    {
        "id": 10,
        "client_id": 4,
        "driver_id": 13,
        "city_id": 12,
        "status": StatusType.CANCELED_BY_DRIVER,
        "request_at": date(2013, 10, 3),
    },
]



def seed_trips_and_users(*, append: bool = False) -> tuple[int, int]:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(
                text(
                    f'TRUNCATE TABLE "{SCHEMA}".trips, "{SCHEMA}".users '
                    "RESTART IDENTITY CASCADE"
                )
            )

        if SEED_USERS:
            session.add_all(User(**row) for row in SEED_USERS)
            session.flush()

        if SEED_TRIPS:
            session.add_all(Trip(**row) for row in SEED_TRIPS)

        session.commit()

        total_users = session.scalar(select(func.count()).select_from(User))
        total_trips = session.scalar(select(func.count()).select_from(Trip))

    return (total_users or 0, total_trips or 0)



def main() -> None:
    parser = argparse.ArgumentParser(description="Seed LC 262 Trips and Users data.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    total_users, total_trips = seed_trips_and_users(append=args.append)
    mode = "appended" if args.append else "reset and seeded"
    print(
        "Seed complete: "
        f"{mode}. Inserted {len(SEED_USERS)} users and {len(SEED_TRIPS)} trips; "
        f"totals now users={total_users}, trips={total_trips}."
    )


if __name__ == "__main__":
    main()
