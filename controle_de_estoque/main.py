from fastapi import FastAPI
from pydantic import BaseModel

# Definindo o modelo de dados para o produto
#o base model é uma classe que define a estrutura dos dados que serão recebidos e enviados pela API. 
#Ele é usado para validar os dados de entrada e saída da API, 
#garantindo que eles estejam no formato correto.
class Produto(BaseModel):
    nome: str
    quantidade: int
    preco: float

app = FastAPI()

#Lista para armazenar os produtos em memória.
estoque = []

@app.get("/")
async def root():
   return {"message": "Controle de Estoque"}

#listando os produtos
@app.get("/produtos", response_model=list[Produto])
async def listar_produtos():
   return estoque

#adicionando produtos
@app.post("/produtos", response_model=Produto)
async def adicionar_produto(produto: Produto):
   estoque.append(produto.model_dump())
   return produto

#atualizando produtos
@app.put("/produtos/{nome}", response_model=Produto)
async def atualizar_produto(nome: str, quant: int, preco: float):
    for produto in estoque:
        if produto["nome"] == nome:
            produto["quantidade"] = quant
            produto["preco"] = preco
            return produto

    return {"message": "Produto não encontrado"}

#removendo produtos
@app.delete("/produtos/{nome}")
async def remover_produto(nome: str):
    for produto in estoque:
        if produto["nome"] == nome:
            estoque.remove(produto)
            return {"message": "Produto removido com sucesso"}

    return {"message": "Produto não encontrado"}