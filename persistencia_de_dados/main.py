from fastapi import Depends, FastAPI, HTTPException
from database import Base, engine
from model import Produto
from sqlalchemy.orm import Session
from database import get_db
from schemas import ProdutoCreate, ProdutoResponse

app = FastAPI()

#aqui estou chamando o database
#Base.metadata.create_all(bind=engine)

# Definindo o modelo de dados para o produto
#o base model é uma classe que define a estrutura dos dados que serão recebidos e enviados pela API. 
#Ele é usado para validar os dados de entrada e saída da API, 
#garantindo que eles estejam no formato correto.
# A validação dos dados agora é feita pelas classes ProdutoCreate e ProdutoResponse, em schemas.py.


#Lista para armazenar os produtos em memória.
# Não será mais utilizada, pois os produtos serão armazenados no banco de dados.


@app.get("/")
async def root():
   return {"message": "Controle de Estoque"}


@app.get("/teste-conexao")
def testar_conexao(db: Session = Depends(get_db)):
    return {"message": "Sessão do banco recebida com sucesso!"}


#listando os produtos
@app.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()


#adicionando produtos
@app.post("/produtos", response_model=ProdutoResponse)
def adicionar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = Produto(
        nome=produto.nome,
        quantidade=produto.quantidade,
        preco=produto.preco
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


#atualizando produtos
@app.put("/produtos/{nome}", response_model=ProdutoResponse)
def atualizar_produto(nome: str, quant: int, preco: float, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.nome == nome).first()
    if produto:
        produto.quantidade = quant
        produto.preco = preco
        db.commit()
        db.refresh(produto)
        return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")


#removendo produtos
@app.delete("/produtos/{nome}")
def remover_produto(nome: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.nome == nome).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()
    return {"message": "Produto removido com sucesso"}
