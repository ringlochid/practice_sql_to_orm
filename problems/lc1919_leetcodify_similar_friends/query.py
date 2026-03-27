from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from database import get_session

from .models import Friendship, Listen, create_tables


def get_similar_friends(session: Session):
    distinct_listens = (
        select(
            Listen.user_id.label("user_id"),
            Listen.song_id.label("song_id"),
            Listen.day.label("day"),
        )
        .distinct()
        .cte("distinct_listens")
    )
    user1_listens = distinct_listens.alias("user1_listens")
    user2_listens = distinct_listens.alias("user2_listens")

    similar_friend_days = (
        select(
            Friendship.user1_id.label("user1_id"),
            Friendship.user2_id.label("user2_id"),
            user1_listens.c.day.label("day"),
        )
        .select_from(Friendship)
        .join(user1_listens, user1_listens.c.user_id == Friendship.user1_id)
        .join(
            user2_listens,
            and_(
                user2_listens.c.user_id == Friendship.user2_id,
                user2_listens.c.song_id == user1_listens.c.song_id,
                user2_listens.c.day == user1_listens.c.day,
            ),
        )
        .group_by(Friendship.user1_id, Friendship.user2_id, user1_listens.c.day)
        .having(func.count() >= 3)
        .cte("similar_friend_days")
    )

    stmt = (
        select(
            similar_friend_days.c.user1_id,
            similar_friend_days.c.user2_id,
        )
        .distinct()
        .order_by(similar_friend_days.c.user1_id, similar_friend_days.c.user2_id)
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    with get_session() as session:
        rows = get_similar_friends(session)

    if not rows:
        print(
            "No rows found. Run `python -m problems.lc1919_leetcodify_similar_friends.seed` first."
        )
        return

    for row in rows:
        print(f"user1_id={row.user1_id} user2_id={row.user2_id} ")


if __name__ == "__main__":
    main()
