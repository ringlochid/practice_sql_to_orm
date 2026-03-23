from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Employee(Base):
    __tablename__ = "Employee"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    salary: Mapped[int] = mapped_column(Integer)
    departmentId: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Department.id", ondelete="CASCADE"),
        nullable=False,
    )

    Department: Mapped["Department"] = relationship(
        "Department", back_populates="Employees"
    )


class Department(Base):
    __tablename__ = "Department"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    Employees: Mapped[list["Employee"]] = relationship(
        "Employee", back_populates="Department"
    )
