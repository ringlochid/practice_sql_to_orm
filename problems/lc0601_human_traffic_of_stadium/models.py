from datetime import datetime

from sqlalchemy import DateTime, Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine

SCHEMA = "lc0601_human_traffic_of_stadium"


class Base(DeclarativeBase):
    pass


class Stadium(Base):
    __tablename__ = "Stadium"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    visit_date: Mapped[datetime] = mapped_column(DateTime)
    people: Mapped[int] = mapped_column(Integer)


def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
