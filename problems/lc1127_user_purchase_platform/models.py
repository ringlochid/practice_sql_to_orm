from datetime import date

from sqlalchemy import CheckConstraint, Date, Integer, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine

SCHEMA = "lc1127_user_purchase_platform"


class Base(DeclarativeBase):
    pass


class Spending(Base):
    __tablename__ = "spending"
    __table_args__ = (
        CheckConstraint(
            "platform IN ('desktop', 'mobile')",
            name="ck_spending_platform",
        ),
        {"schema": SCHEMA},
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spend_date: Mapped[date] = mapped_column(Date, primary_key=True)
    platform: Mapped[str] = mapped_column(String, primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)


def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
