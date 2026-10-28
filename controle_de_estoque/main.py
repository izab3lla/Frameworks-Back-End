from fastapi import FastAPI
from pydantic import BaseModel

class Produto(BaseModel):
    nome: str
    quantidade: int
    preco: float

app = FastAPI()

estoque = []

@app.get("/")
async def root():
   return {"message": "Controle de Estoque"}

#listando os produtos
@app.get("/produtos")
async def listar_produtos():
   return estoque

@app.post("/produtos", response_model=Produto)
async def adicionar_produto(produto: Produto):
   estoque.append(produto.model_dump())
   return produto

@app.put("/produtos/{nome}")
async def atualizar_produto(nome: str, quant: int, preco: float):
    for produto in estoque:
        if produto["nome"] == nome:
            produto["quantidade"] = quant
            produto["preco"] = preco
            return produto

    return {"message": "Produto não encontrado"}

@app.delete("/produtos/{nome}")
async def remover_produto(nome: str):
    for produto in estoque:
        if produto["nome"] == nome:
            estoque.remove(produto)
            return {"message": "Produto removido com sucesso"}

    return {"message": "Produto não encontrado"}