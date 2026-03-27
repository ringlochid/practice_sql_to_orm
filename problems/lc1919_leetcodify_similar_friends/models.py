from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database import engine

SCHEMA = "lc1919_leetcodify_similar_friends"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)

    friendship_from: Mapped[list["Friendship"]] = relationship(
        "Friendship",
        foreign_keys="Friendship.user1_id",
        back_populates="user_from",
    )
    friendship_to: Mapped[list["Friendship"]] = relationship(
        "Friendship",
        foreign_keys="Friendship.user2_id",
        back_populates="user_to",
    )


class Friendship(Base):
    __tablename__ = "friendships"
    __table_args__ = (
        CheckConstraint("user1_id < user2_id", "ck_user1_id_gt_user2_id"),
        {"schema": SCHEMA},
    )

    user1_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.users.id"), primary_key=True
    )
    user2_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{SCHEMA}.users.id"), primary_key=True
    )

    user_from: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user1_id],
        back_populates="friendship_from",
    )
    user_to: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user2_id],
        back_populates="friendship_to",
    )


class Listen(Base):
    __tablename__ = "listens"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{SCHEMA}.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    song_id: Mapped[int] = mapped_column(Integer, nullable=False)
    day: Mapped[date] = mapped_column(Date, nullable=False)


def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
