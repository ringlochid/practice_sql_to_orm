from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

SCHEMA = "lc0601_human_traffic_of_stadiumu"


class Base(DeclarativeBase):
    pass


class Stadium(Base):
    __tablename__ = "Stadium"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    visited_date: Mapped[datetime] = mapped_column(DateTime)
    people: Mapped[int] = mapped_column(Integer)
