import argparse
from datetime import datetime

from sqlalchemy import func, select, text

from database import get_session

from .models import SCHEMA, Stadium, create_tables

SEED_STADIUM = [
    {"id": 1, "visit_date": datetime(2017, 1, 1), "people": 10},
    {"id": 2, "visit_date": datetime(2017, 1, 2), "people": 109},
    {"id": 3, "visit_date": datetime(2017, 1, 3), "people": 150},
    {"id": 4, "visit_date": datetime(2017, 1, 4), "people": 99},
    {"id": 5, "visit_date": datetime(2017, 1, 5), "people": 145},
    {"id": 6, "visit_date": datetime(2017, 1, 6), "people": 1455},
    {"id": 7, "visit_date": datetime(2017, 1, 7), "people": 199},
    {"id": 8, "visit_date": datetime(2017, 1, 9), "people": 188},
]


def seed_human_traffic_of_stadium(*, append: bool = False) -> tuple[int, int]:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(
                text(f'TRUNCATE TABLE "{SCHEMA}"."Stadium" RESTART IDENTITY CASCADE')
            )
            rows_to_insert = SEED_STADIUM
        else:
            existing_ids = set(session.scalars(select(Stadium.id)).all())
            rows_to_insert = [row for row in SEED_STADIUM if row["id"] not in existing_ids]

        session.add_all(
            Stadium(
                id=row["id"],
                visit_date=row["visit_date"],
                people=row["people"],
            )
            for row in rows_to_insert
        )
        session.commit()

        total_stadium = session.scalar(select(func.count()).select_from(Stadium))

    return len(rows_to_insert), total_stadium or 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed Human Traffic of Stadium example data."
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append only missing seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    inserted_stadium, total_stadium = seed_human_traffic_of_stadium(append=args.append)
    mode = "appended" if args.append else "reset and seeded"
    print(
        "Seed complete: "
        f"{mode}. Inserted {inserted_stadium} stadium entries; "
        f"totals now stadium={total_stadium}."
    )


if __name__ == "__main__":
    main()
