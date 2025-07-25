from src.db import intpk, Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Record(Base):
    __tablename__ = 'records'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(49),
        nullable=False
    )
    date: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
