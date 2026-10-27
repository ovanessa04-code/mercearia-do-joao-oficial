from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models.produtos import Produto


router = APIRouter(prefix="/produtos", tags=["Produtos"])


class ProdutoEntrada(BaseModel):
    nome_produto: str = Field(min_length=1, max_length=150)
    categoria: int
    quantidade_estoque: int
    preco:Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    @field_validator("nome_produto")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome não pode ficar vazio.")
        return valor


class ProdutoSaida(ProdutoEntrada):
    model_config = ConfigDict(from_attributes=True)

    id_produto: int


def buscar_produto(id_produto: int, db: Session) -> Produto:
    produto = db.get(Produto, id_produto)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado.",
        )
    return produto


@router.post(
    "",
    response_model=ProdutoSaida,
    status_code=status.HTTP_201_CREATED,
)
def cadastrar_produto(
    dados: ProdutoEntrada,
    db: Session = Depends(get_db),
) -> Produto: 
    produto= Produto(**dados.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto 


@router.get("", response_model=list[ProdutoSaida])
def listar_produtos(db: Session = Depends(get_db)) -> list[Produto]:
    consulta = select(Produto).order_by(Produto.id_produto)
    return list(db.scalars(consulta).all())


@router.get("/{id_produto}", response_model=ProdutoSaida)
def consultar_produto(
    id_produto: int,
    db: Session = Depends(get_db),
) -> Produto:
    return buscar_produto(id_produto= db)


@router.put("/{id_produto}", response_model=ProdutoSaida)
def atualizar_produto(
    id_produto: int,
    dados: ProdutoEntrada,
    db: Session = Depends(get_db),
) -> Produto:
    produto = buscar_produto(id_produto, db)
    produto.nome_produto = dados.nome_produto
    produto.categoria = dados.categoria
    produto.quantidade_estoque = dados.quantidade_estoque
    produto.preco = dados.preco
    db.commit()
    db.refresh(produto)
    return produto


@router.delete(
    "/{id_produto}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_produto(
    id_produto: int,
    db: Session = Depends(get_db),
) -> Response:
    produto = buscar_produto(id_produto, db)
    db.delete(produto)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
