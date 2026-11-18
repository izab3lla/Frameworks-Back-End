from fastapi import Depends, FastAPI, HTTPException
from database import Base, engine
from model import Produto
from sqlalchemy.orm import Session
from database import get_db
from schemas import ProdutoCreate, ProdutoResponse

#tags usadas no swagger pra organizar as rotas
tags_metadata = [
    {
        "name": "Geral",
        "description": "Rotas iniciais e de verificação da API.",
    },
    {
        "name": "Produtos",
        "description": "Cadastro, listagem, atualização e remoção de produtos.",
    },
]

app = FastAPI(
    title="Controle de Estoque",
    description="API REST para controle de estoque de produtos com persistência em SQLite.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

#aqui estou chamando o database
#Base.metadata.create_all(bind=engine)

# Definindo o modelo de dados para o produto
#o base model é uma classe que define a estrutura dos dados que serão recebidos e enviados pela API. 
#Ele é usado para validar os dados de entrada e saída da API, 
#garantindo que eles estejam no formato correto.
# A validação dos dados agora é feita pelas classes ProdutoCreate e ProdutoResponse, em schemas.py.


#Lista para armazenar os produtos em memória.
# Não será mais utilizada, pois os produtos serão armazenados no banco de dados.


@app.get(
    "/",
    tags=["Geral"],
    summary="Mensagem inicial",
    description="Retorna uma mensagem simples para confirmar que a API está no ar.",
    responses={200: {"description": "API respondendo normalmente"}},
)
async def root():
    """Rota inicial da aplicação."""
    return {"message": "Controle de Estoque"}


@app.get(
    "/teste-conexao",
    tags=["Geral"],
    summary="Testar conexão com o banco",
    description="Verifica se a sessão do banco de dados está sendo criada corretamente.",
    responses={200: {"description": "Sessão do banco recebida com sucesso"}},
)
def testar_conexao(db: Session = Depends(get_db)):
    """Testa se o Depends está entregando a sessão do banco."""
    return {"message": "Sessão do banco recebida com sucesso!"}


#listando os produtos
@app.get(
    "/produtos",
    response_model=list[ProdutoResponse],
    tags=["Produtos"],
    summary="Listar produtos",
    description="Retorna todos os produtos cadastrados no banco de dados.",
    responses={200: {"description": "Lista de produtos retornada com sucesso"}},
)
def listar_produtos(db: Session = Depends(get_db)):
    """Lista todos os produtos do estoque."""
    return db.query(Produto).all()


#adicionando produtos
@app.post(
    "/produtos",
    response_model=ProdutoResponse,
    tags=["Produtos"],
    summary="Cadastrar produto",
    description="Recebe nome, quantidade e preço e salva um novo produto no banco.",
    responses={
        200: {"description": "Produto cadastrado com sucesso"},
        422: {"description": "Dados inválidos enviados no body"},
    },
)
def adicionar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """Cadastra um novo produto no estoque."""
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
@app.put(
    "/produtos/{nome}",
    response_model=ProdutoResponse,
    tags=["Produtos"],
    summary="Atualizar produto",
    description="Atualiza a quantidade e o preço de um produto a partir do nome.",
    responses={
        200: {"description": "Produto atualizado com sucesso"},
        404: {"description": "Produto não encontrado"},
    },
)
def atualizar_produto(nome: str, quant: int, preco: float, db: Session = Depends(get_db)):
    """Atualiza quantidade e preço de um produto existente."""
    produto = db.query(Produto).filter(Produto.nome == nome).first()
    if produto:
        produto.quantidade = quant
        produto.preco = preco
        db.commit()
        db.refresh(produto)
        return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")


#removendo produtos
@app.delete(
    "/produtos/{nome}",
    tags=["Produtos"],
    summary="Remover produto",
    description="Remove um produto do estoque pelo nome informado na URL.",
    responses={
        200: {"description": "Produto removido com sucesso"},
        404: {"description": "Produto não encontrado"},
    },
)
def remover_produto(nome: str, db: Session = Depends(get_db)):
    """Remove um produto do banco pelo nome."""
    produto = db.query(Produto).filter(Produto.nome == nome).first()
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()
    return {"message": "Produto removido com sucesso"}
