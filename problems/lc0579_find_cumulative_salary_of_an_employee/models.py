from sqlalchemy import Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine

SCHEMA = "lc0579_find_cumulative_salary_of_an_employee"


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    month: Mapped[int] = mapped_column(Integer, primary_key=True)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)


def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
