from sqlalchemy import and_, case, func, literal, select, true, union_all
from sqlalchemy.orm import Session

from database import get_session

from .models import Spending, create_tables


def get_user_purchase_platform(session: Session):
    per_user = (
        select(
            Spending.spend_date,
            Spending.user_id,
            case((func.count() >= 2, "both"), else_=func.max(Spending.platform)).label(
                "platform"
            ),
            func.sum(Spending.amount).label("amount"),
        )
        .group_by(Spending.spend_date, Spending.user_id)
        .cte("per_user")
    )

    all_dates = select(Spending.spend_date).distinct().cte("all_dates")

    all_platforms = union_all(
        select(literal("mobile").label("platform")),
        select(literal("desktop").label("platform")),
        select(literal("both").label("platform")),
    ).cte("all_platforms")

    stmt = (
        select(
            all_dates.c.spend_date,
            all_platforms.c.platform,
            func.sum(func.coalesce(per_user.c.amount, 0)).label("total_amount"),
            func.count(per_user.c.user_id).label("total_users"),
        )
        .select_from(all_dates)
        .join(all_platforms, true())
        .outerjoin(
            per_user,
            and_(
                all_dates.c.spend_date == per_user.c.spend_date,
                all_platforms.c.platform == per_user.c.platform,
            ),
        )
        .group_by(all_dates.c.spend_date, all_platforms.c.platform)
    )

    return session.execute(stmt).all()


def main() -> None:
    create_tables()

    try:
        with get_session() as session:
            rows = get_user_purchase_platform(session)
    except NotImplementedError as exc:
        print(exc)
        return

    if not rows:
        print(
            "No rows found. Run `python -m problems.lc1127_user_purchase_platform.seed` first."
        )
        return

    for row in rows:
        print(
            f"spend_date={row.spend_date} platform={row.platform} "
            f"total_amount={row.total_amount} total_users={row.total_users}"
        )


if __name__ == "__main__":
    main()
