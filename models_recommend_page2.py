from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


friend_relation = Table(
    "friend_relation",
    Base.metadata,
    Column("user1_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("user2_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    Friends: Mapped[list["User"]] = relationship(
        "User",
        secondary=friend_relation,
        primaryjoin=id == friend_relation.c.user1_id,
        secondaryjoin=id == friend_relation.c.user2_id,
    )


class Likes(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id"))


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
