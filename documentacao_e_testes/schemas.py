from pydantic import BaseModel

class ProdutoCreate(BaseModel):
    nome: str
    quantidade: int
    preco: float

class ProdutoResponse(BaseModel):
    nome: str
    quantidade: int
    preco: float

    class Config:
        from_attributes = True