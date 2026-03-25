from sqlalchemy.orm import Session

from database import get_session

from .models import create_tables


def get_user_purchase_platform(session: Session):
    """Translate query.sql into SQLAlchemy here."""
    raise NotImplementedError(
        "TODO: translate problems.lc1127_user_purchase_platform.query.sql into SQLAlchemy."
    )


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
