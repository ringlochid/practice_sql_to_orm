from sqlalchemy import ForeignKey, Index, Integer, String, desc, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database import engine

SCHEMA = "lc0185_department_top_three_salaries"


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="department",
        cascade="all, delete-orphan",
    )


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        Index(
            "ix_employees_department_salary_desc_name",
            "department_id",
            desc("salary"),
            "name",
        ),
        {"schema": SCHEMA},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(f"{SCHEMA}.departments.id", ondelete="CASCADE"),
        nullable=False,
    )

    department: Mapped[Department] = relationship(
        "Department",
        back_populates="employees",
    )


def create_tables() -> None:
    with engine.begin() as connection:
        connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))
    Base.metadata.create_all(bind=engine)
