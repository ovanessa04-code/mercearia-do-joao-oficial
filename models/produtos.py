from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Identity, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Produto(Base):
    __tablename__ = "produtos"
    __table_args__ = {"schema": "public"}

    id_produto: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
    )
    nome_produto: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    categoria: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    quantidade_estoque: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    preco: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )
