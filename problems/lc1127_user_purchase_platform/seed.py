import argparse
from datetime import date

from sqlalchemy import func, select, text

from database import get_session

from .models import SCHEMA, Spending, create_tables

SEED_SPENDING: list[dict[str, int | str | date]] = [
    {"user_id": 1, "spend_date": date(2019, 7, 1), "platform": "mobile", "amount": 100},
    {
        "user_id": 1,
        "spend_date": date(2019, 7, 1),
        "platform": "desktop",
        "amount": 100,
    },
    {"user_id": 2, "spend_date": date(2019, 7, 1), "platform": "mobile", "amount": 100},
    {"user_id": 2, "spend_date": date(2019, 7, 2), "platform": "mobile", "amount": 100},
    {
        "user_id": 3,
        "spend_date": date(2019, 7, 1),
        "platform": "desktop",
        "amount": 100,
    },
    {
        "user_id": 3,
        "spend_date": date(2019, 7, 2),
        "platform": "desktop",
        "amount": 100,
    },
]


def seed_user_purchase_platform(*, append: bool = False) -> tuple[int, int]:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(
                text(f'TRUNCATE TABLE "{SCHEMA}".spending RESTART IDENTITY CASCADE')
            )
            rows_to_insert = SEED_SPENDING
        else:
            existing_keys = set(
                session.execute(
                    select(Spending.user_id, Spending.spend_date, Spending.platform)
                ).all()
            )
            rows_to_insert = [
                row
                for row in SEED_SPENDING
                if (row["user_id"], row["spend_date"], row["platform"])
                not in existing_keys
            ]

        if rows_to_insert:
            session.add_all(Spending(**row) for row in rows_to_insert)

        session.commit()

        inserted = len(rows_to_insert)
        total_rows = session.scalar(select(func.count()).select_from(Spending)) or 0

    return inserted, total_rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed User Purchase Platform data.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append only missing seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    inserted, total_rows = seed_user_purchase_platform(append=args.append)
    mode = "appended" if args.append else "reset and seeded"
    print(
        "Seed complete: "
        f"{mode}. Inserted {inserted} spending rows; totals now spending={total_rows}."
    )


if __name__ == "__main__":
    main()
