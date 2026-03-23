from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    company: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    salary: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    __table_args__ = (CheckConstraint("salary > 0", name="check_salary_positive"),)
