from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Identity, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Cliente(Base):
    __tablename__ = "clientes"
    __table_args__ = {"schema": "public"}

    id_cliente: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
    )
    nome_cliente: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    data_nascimento: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    valor_limite: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
