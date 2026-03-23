from sqlalchemy import Column, ForeignKey, Integer, String, Table, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database import engine

SCHEMA = "lc1892_page_recommendations_ii"


class Base(DeclarativeBase):
    pass


friendships = Table(
    "friendships",
    Base.metadata,
    Column("user_id", Integer, ForeignKey(f"{SCHEMA}.users.id"), primary_key=True),
    Column("friend_id", Integer, ForeignKey(f"{SCHEMA}.users.id"), primary_key=True),
    schema=SCHEMA,
)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    friends: Mapped[list["User"]] = relationship(
        "User",
        secondary=friendships,
        primaryjoin=id == friendships.c.user_id,
        secondaryjoin=id == friendships.c.friend_id,
    )


class Page(Base):
    __tablename__ = "pages"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.users.id"),
        nullable=False,
    )
    page_id: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.pages.id"),
        nullable=False,
    )


def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
