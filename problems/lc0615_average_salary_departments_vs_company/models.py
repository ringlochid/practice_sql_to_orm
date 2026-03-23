from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database import engine

SCHEMA = "lc0615_average_salary_departments_vs_company"


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {"schema": SCHEMA}

    employee_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    department_id: Mapped[int] = mapped_column(Integer, nullable=False)

    salaries: Mapped[list["Salary"]] = relationship(
        "Salary",
        back_populates="employee",
        cascade="all, delete-orphan",
    )


class Salary(Base):
    __tablename__ = "salaries"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{SCHEMA}.employees.employee_id", ondelete="CASCADE"),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    pay_date: Mapped[date] = mapped_column(Date, nullable=False)

    employee: Mapped[Employee] = relationship("Employee", back_populates="salaries")


def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
