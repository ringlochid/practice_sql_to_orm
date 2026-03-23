from sqlalchemy import func, select, tuple_, union_all
from sqlalchemy.orm import Session

from database import create_tables, get_session
from models_recommend_page2 import Likes, friend_relation


def get_recommandations(session: Session):
    outgoing_friends = select(
        friend_relation.c.user1_id.label("user_id"),
        friend_relation.c.user2_id.label("friend_id"),
    )

    incoming_friends = select(
        friend_relation.c.user2_id.label("user_id"),
        friend_relation.c.user1_id.label("friend_id"),
    )

    friends = union_all(outgoing_friends, incoming_friends).cte("friends")
    liked_pages = select(Likes.user_id, Likes.page_id).subquery()

    stmt = (
        select(
            friends.c.user_id,
            Likes.page_id,
            func.count().label("friends_likes"),
        )
        .select_from(friends)
        .join(Likes, friends.c.friend_id == Likes.user_id)
        .where(~tuple_(friends.c.user_id, Likes.page_id).in_(liked_pages.select()))
        .group_by(friends.c.user_id, Likes.page_id)
        .order_by(friends.c.user_id, Likes.page_id)
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    with get_session() as session:
        rows = get_recommandations(session)

    if not rows:
        print("No rows found. Run seed_recommand_page2.py first.")
        return

    for row in rows:
        print(
            f"user_id={row.user_id} page_id={row.page_id} friends_likes={row.friends_likes}"
        )


if __name__ == "__main__":
    main()
