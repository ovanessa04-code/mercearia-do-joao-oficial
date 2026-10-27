from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models.clientes import Cliente


router = APIRouter(prefix="/clientes", tags=["Clientes"])


class ClienteEntrada(BaseModel):
    nome_cliente: str = Field(min_length=1, max_length=150)
    data_nascimento: date
    valor_limite: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    @field_validator("nome_cliente")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome não pode ficar vazio.")
        return valor


class ClienteSaida(ClienteEntrada):
    model_config = ConfigDict(from_attributes=True)

    id_cliente: int


def buscar_cliente(id_cliente: int, db: Session) -> Cliente:
    cliente = db.get(Cliente, id_cliente)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado.",
        )
    return cliente


@router.post(
    "",
    response_model=ClienteSaida,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_cliente(
    dados: ClienteEntrada,
    db: Session = Depends(get_db),
) -> Cliente:
    cliente = Cliente(**dados.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.get("", response_model=list[ClienteSaida])
def listar_clientes(db: Session = Depends(get_db)) -> list[Cliente]:
    consulta = select(Cliente).order_by(Cliente.id_cliente)
    return list(db.scalars(consulta).all())


@router.get("/{id_cliente}", response_model=ClienteSaida)
def consultar_cliente(
    id_cliente: int,
    db: Session = Depends(get_db),
) -> Cliente:
    return buscar_cliente(id_cliente, db)


@router.put("/{id_cliente}", response_model=ClienteSaida)
def atualizar_cliente(
    id_cliente: int,
    dados: ClienteEntrada,
    db: Session = Depends(get_db),
) -> Cliente:
    cliente = buscar_cliente(id_cliente, db)
    cliente.nome_cliente = dados.nome_cliente
    cliente.data_nascimento = dados.data_nascimento
    cliente.valor_limite = dados.valor_limite
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete(
    "/{id_cliente}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_cliente(
    id_cliente: int,
    db: Session = Depends(get_db),
) -> Response:
    cliente = buscar_cliente(id_cliente, db)
    db.delete(cliente)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
