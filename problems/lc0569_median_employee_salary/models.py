from sqlalchemy import CheckConstraint, Index, Integer, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine

SCHEMA = "lc0569_median_employee_salary"


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        Index("ix_company_salary_id", "company", "salary", "id"),
        CheckConstraint("salary > 0", name="check_salary_positive"),
        {"schema": SCHEMA},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    salary: Mapped[int] = mapped_column(Integer, nullable=False, index=True)


def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
