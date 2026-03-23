from sqlalchemy import func, select, tuple_, union_all
from sqlalchemy.orm import Session

from database import get_session

from .models import Like, create_tables, friendships


def get_page_recommendations(session: Session):
    outgoing_friends = select(
        friendships.c.user_id.label("user_id"),
        friendships.c.friend_id.label("friend_id"),
    )

    incoming_friends = select(
        friendships.c.friend_id.label("user_id"),
        friendships.c.user_id.label("friend_id"),
    )

    all_friendships = union_all(outgoing_friends, incoming_friends).cte(
        "all_friendships"
    )
    liked_pages = select(Like.user_id, Like.page_id).subquery()

    stmt = (
        select(
            all_friendships.c.user_id,
            Like.page_id,
            func.count().label("friends_likes"),
        )
        .select_from(all_friendships)
        .join(Like, all_friendships.c.friend_id == Like.user_id)
        .where(~tuple_(all_friendships.c.user_id, Like.page_id).in_(liked_pages.select()))
        .group_by(all_friendships.c.user_id, Like.page_id)
        .order_by(all_friendships.c.user_id, Like.page_id)
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    with get_session() as session:
        rows = get_page_recommendations(session)

    if not rows:
        print(
            "No rows found. Run `python -m problems.lc1892_page_recommendations_ii.seed` first."
        )
        return

    for row in rows:
        print(
            f"user_id={row.user_id} page_id={row.page_id} friends_likes={row.friends_likes}"
        )


if __name__ == "__main__":
    main()
