import argparse
from datetime import date

from sqlalchemy import func, select, text

from database import get_session

from .models import Friendship, Listen, SCHEMA, User, create_tables

SEED_USERS = [
    {"id": 1, "name": "User 1"},
    {"id": 2, "name": "User 2"},
    {"id": 3, "name": "User 3"},
    {"id": 4, "name": "User 4"},
    {"id": 5, "name": "User 5"},
]

SEED_FRIENDSHIPS = [
    {"user1_id": 1, "user2_id": 2},
    {"user1_id": 2, "user2_id": 4},
    {"user1_id": 2, "user2_id": 5},
]

SEED_LISTENS: list[dict[str, int | date]] = [
    {"user_id": 1, "song_id": 10, "day": date(2021, 3, 15)},
    {"user_id": 1, "song_id": 11, "day": date(2021, 3, 15)},
    {"user_id": 1, "song_id": 12, "day": date(2021, 3, 15)},
    {"user_id": 2, "song_id": 10, "day": date(2021, 3, 15)},
    {"user_id": 2, "song_id": 11, "day": date(2021, 3, 15)},
    {"user_id": 2, "song_id": 12, "day": date(2021, 3, 15)},
    {"user_id": 3, "song_id": 10, "day": date(2021, 3, 15)},
    {"user_id": 3, "song_id": 11, "day": date(2021, 3, 15)},
    {"user_id": 3, "song_id": 12, "day": date(2021, 3, 15)},
    {"user_id": 4, "song_id": 10, "day": date(2021, 3, 15)},
    {"user_id": 4, "song_id": 11, "day": date(2021, 3, 15)},
    {"user_id": 4, "song_id": 13, "day": date(2021, 3, 15)},
    {"user_id": 5, "song_id": 10, "day": date(2021, 3, 16)},
    {"user_id": 5, "song_id": 11, "day": date(2021, 3, 16)},
    {"user_id": 5, "song_id": 12, "day": date(2021, 3, 16)},
]


def seed_similar_friends(*, append: bool = False) -> dict[str, int]:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(
                text(
                    f'TRUNCATE TABLE "{SCHEMA}".listens, "{SCHEMA}".friendships, '
                    f'"{SCHEMA}".users RESTART IDENTITY CASCADE'
                )
            )

        existing_user_ids = set(session.scalars(select(User.id)).all())
        existing_friendships = {
            (row.user1_id, row.user2_id)
            for row in session.execute(
                select(Friendship.user1_id, Friendship.user2_id)
            ).all()
        }
        existing_listens = {
            (row.user_id, row.song_id, row.day)
            for row in session.execute(
                select(Listen.user_id, Listen.song_id, Listen.day)
            ).all()
        }

        users_to_add = [
            User(**row) for row in SEED_USERS if row["id"] not in existing_user_ids
        ]
        friendships_to_add = [
            Friendship(**row)
            for row in SEED_FRIENDSHIPS
            if (row["user1_id"], row["user2_id"]) not in existing_friendships
        ]
        listens_to_add = [
            Listen(**row)
            for row in SEED_LISTENS
            if (row["user_id"], row["song_id"], row["day"]) not in existing_listens
        ]

        if users_to_add:
            session.add_all(users_to_add)
            session.flush()

        if friendships_to_add:
            session.add_all(friendships_to_add)
        if listens_to_add:
            session.add_all(listens_to_add)

        session.commit()

        totals = {
            "users": session.scalar(select(func.count()).select_from(User)) or 0,
            "friendships": session.scalar(select(func.count()).select_from(Friendship))
            or 0,
            "listens": session.scalar(select(func.count()).select_from(Listen)) or 0,
        }

    return totals


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Leetcodify Similar Friends data.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append missing seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    totals = seed_similar_friends(append=args.append)
    mode = "appended missing rows" if args.append else "reset and seeded"
    print(
        "Seed complete: "
        f"{mode}. Totals now users={totals['users']}, "
        f"friendships={totals['friendships']}, listens={totals['listens']}."
    )


if __name__ == "__main__":
    main()
