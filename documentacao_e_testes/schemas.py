from pydantic import BaseModel

#ProdutoCreate é o que a API recebe quando cadastra um produto
#serve pra validar se o nome, quantidade e preco vieram certos
class ProdutoCreate(BaseModel):
    nome: str
    quantidade: int
    preco: float

#ProdutoResponse é o que a API devolve nas respostas
#from_attributes = True deixa o pydantic ler direto do model do sqlalchemy
class ProdutoResponse(BaseModel):
    nome: str
    quantidade: int
    preco: float

    class Config:
        from_attributes = True
