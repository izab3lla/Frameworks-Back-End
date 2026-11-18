#testes da API usando TestClient e Pytest
#baseado na documentação: https://fastapi.tiangolo.com/tutorial/testing/

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from model import Produto

#banco separado só pra não bagunçar o estoque.db real
#a url aqui vai informar que vai ser usado o sqlite de teste
sql_url_teste = "sqlite:///./teste.db"

#mesma ideia do database.py, só que apontando pro teste.db
engine_teste = create_engine(sql_url_teste, connect_args={"check_same_thread": False})
SessionTeste = sessionmaker(autocommit=False, autoflush=False, bind=engine_teste)

#cria as tabelas no banco de teste
Base.metadata.create_all(bind=engine_teste)


#essa função troca o get_db da aplicação pelo banco de teste
#assim os testes não mexem no estoque.db
def override_get_db():
    db = SessionTeste() #aqui vai criar uma nova sessão de conexão com o bd de teste
    try:
        yield db #vai entregar a sessão pra qm chamou
    finally:
        db.close() #aqui fecha e libera os recursos dela


#aqui eu sobrescrevo a dependencia do banco
app.dependency_overrides[get_db] = override_get_db

#o TestClient simula as requisições sem precisar subir o servidor
client = TestClient(app)


#função pra limpar os produtos entre um teste e outro
#pra um teste não atrapalhar o resultado do outro
def limpar_produtos():
    db = SessionTeste()
    db.query(Produto).delete()
    db.commit()
    db.close()


#testando se a rota GET / retorna status 200
def test_root_status_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Controle de Estoque"}


#testando se a listagem de produtos também retorna 200
def test_listar_produtos_status_200():
    limpar_produtos()
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == [] #lista vazia porque limpei o banco


#testando o cadastro de um produto
def test_adicionar_produto():
    limpar_produtos()
    response = client.post(
        "/produtos",
        json={"nome": "Caderno", "quantidade": 10, "preco": 15.5},
    )
    assert response.status_code == 200
    assert response.json() == {
        "nome": "Caderno",
        "quantidade": 10,
        "preco": 15.5,
    }


#testando o erro 404 quando tenta atualizar um produto que não existe
def test_atualizar_produto_404():
    limpar_produtos()
    response = client.put("/produtos/ProdutoInexistente?quant=1&preco=9.9")
    assert response.status_code == 404
    assert response.json() == {"detail": "Produto não encontrado"}


#testando o erro 404 quando tenta remover um produto que não existe
def test_remover_produto_404():
    limpar_produtos()
    response = client.delete("/produtos/ProdutoInexistente")
    assert response.status_code == 404
    assert response.json() == {"detail": "Produto não encontrado"}


#aqui eu testo o fluxo completo: cadastrar, atualizar e remover
def test_atualizar_e_remover_produto():
    limpar_produtos()

    #primeiro cadastro o produto
    client.post(
        "/produtos",
        json={"nome": "Caneta", "quantidade": 5, "preco": 2.0},
    )

    #depois atualizo a quantidade e o preço
    response_put = client.put("/produtos/Caneta?quant=8&preco=3.5")
    assert response_put.status_code == 200
    assert response_put.json() == {
        "nome": "Caneta",
        "quantidade": 8,
        "preco": 3.5,
    }

    #por ultimo removo o produto
    response_delete = client.delete("/produtos/Caneta")
    assert response_delete.status_code == 200
    assert response_delete.json() == {"message": "Produto removido com sucesso"}
