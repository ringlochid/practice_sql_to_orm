import argparse

from sqlalchemy import func, select, text

from database import get_session

from .models import Like, Page, SCHEMA, User, create_tables, friendships

SEED_USERS = [
    {"id": 1, "name": "User 1"},
    {"id": 2, "name": "User 2"},
    {"id": 3, "name": "User 3"},
    {"id": 4, "name": "User 4"},
    {"id": 5, "name": "User 5"},
    {"id": 6, "name": "User 6"},
]

SEED_PAGES = [
    {"id": 11, "title": "Page 11"},
    {"id": 23, "title": "Page 23"},
    {"id": 24, "title": "Page 24"},
    {"id": 33, "title": "Page 33"},
    {"id": 56, "title": "Page 56"},
    {"id": 77, "title": "Page 77"},
    {"id": 88, "title": "Page 88"},
]

SEED_FRIENDSHIPS = [
    {"user_id": 1, "friend_id": 2},
    {"user_id": 1, "friend_id": 3},
    {"user_id": 1, "friend_id": 4},
    {"user_id": 2, "friend_id": 3},
    {"user_id": 2, "friend_id": 4},
    {"user_id": 2, "friend_id": 5},
    {"user_id": 6, "friend_id": 1},
]

SEED_LIKES = [
    {"user_id": 1, "page_id": 88},
    {"user_id": 2, "page_id": 23},
    {"user_id": 3, "page_id": 24},
    {"user_id": 4, "page_id": 56},
    {"user_id": 5, "page_id": 11},
    {"user_id": 6, "page_id": 33},
    {"user_id": 2, "page_id": 77},
    {"user_id": 3, "page_id": 77},
    {"user_id": 6, "page_id": 88},
]


def seed_page_recommendations(*, append: bool = False) -> dict[str, int]:
    create_tables()

    with get_session() as session:
        if not append:
            session.execute(
                text(
                    f'TRUNCATE TABLE "{SCHEMA}".likes, "{SCHEMA}".friendships, '
                    f'"{SCHEMA}".pages, "{SCHEMA}".users RESTART IDENTITY CASCADE'
                )
            )

        existing_user_ids = set(session.scalars(select(User.id)).all())
        existing_page_ids = set(session.scalars(select(Page.id)).all())
        existing_friendships = {
            (row.user_id, row.friend_id)
            for row in session.execute(
                select(friendships.c.user_id, friendships.c.friend_id)
            ).all()
        }
        existing_likes = {
            (row.user_id, row.page_id)
            for row in session.execute(select(Like.user_id, Like.page_id)).all()
        }

        users_to_add = [
            User(**row) for row in SEED_USERS if row["id"] not in existing_user_ids
        ]
        pages_to_add = [
            Page(**row) for row in SEED_PAGES if row["id"] not in existing_page_ids
        ]
        friendships_to_add = [
            row
            for row in SEED_FRIENDSHIPS
            if (row["user_id"], row["friend_id"]) not in existing_friendships
        ]
        likes_to_add = [
            Like(**row)
            for row in SEED_LIKES
            if (row["user_id"], row["page_id"]) not in existing_likes
        ]

        if users_to_add:
            session.add_all(users_to_add)
        if pages_to_add:
            session.add_all(pages_to_add)
        if users_to_add or pages_to_add:
            session.flush()

        if friendships_to_add:
            session.execute(friendships.insert(), friendships_to_add)
        if likes_to_add:
            session.add_all(likes_to_add)

        session.commit()

        totals = {
            "users": session.scalar(select(func.count()).select_from(User)) or 0,
            "pages": session.scalar(select(func.count()).select_from(Page)) or 0,
            "friendships": session.scalar(select(func.count()).select_from(friendships))
            or 0,
            "likes": session.scalar(select(func.count()).select_from(Like)) or 0,
        }

    return totals


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Page Recommendations II data.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append missing seed rows instead of clearing existing rows first.",
    )
    args = parser.parse_args()

    totals = seed_page_recommendations(append=args.append)
    mode = "appended missing rows" if args.append else "reset and seeded"
    print(
        "Seed complete: "
        f"{mode}. Totals now users={totals['users']}, pages={totals['pages']}, "
        f"friendships={totals['friendships']}, likes={totals['likes']}."
    )


if __name__ == "__main__":
    main()
