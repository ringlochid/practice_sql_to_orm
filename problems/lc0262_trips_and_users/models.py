from datetime import date
from enum import Enum as PyEnum

from sqlalchemy import Date, Enum, ForeignKey, Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database import engine


class UserType(str, PyEnum):
    CLIENT = "client"
    DRIVER = "driver"


class StatusType(str, PyEnum):
    COMPLETED = "completed"
    CANCELED_BY_CLIENT = "canceled_by_client"
    CANCELED_BY_DRIVER = "canceled_by_driver"


SCHEMA = "lc0262_trips_and_users"


class Base(DeclarativeBase):
    pass


class Trip(Base):
    __tablename__ = "trips"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{SCHEMA}.users.id"),
        nullable=False,
    )
    driver_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{SCHEMA}.users.id"),
        nullable=False,
    )
    city_id: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[StatusType] = mapped_column(
        Enum(StatusType, name="status_type", native_enum=True), nullable=False
    )
    request_at: Mapped[date] = mapped_column(Date, nullable=False)

    client: Mapped["User"] = relationship(
        "User", foreign_keys=[client_id], back_populates="trips_as_client"
    )
    driver: Mapped["User"] = relationship(
        "User", foreign_keys=[driver_id], back_populates="trips_as_driver"
    )


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    banned: Mapped[bool] = mapped_column(nullable=False)
    role: Mapped[UserType] = mapped_column(
        Enum(UserType, name="user_type", native_enum=True), nullable=False
    )

    trips_as_client: Mapped[list[Trip]] = relationship(
        "Trip", foreign_keys=[Trip.client_id], back_populates="client"
    )
    trips_as_driver: Mapped[list[Trip]] = relationship(
        "Trip", foreign_keys=[Trip.driver_id], back_populates="driver"
    )



def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
