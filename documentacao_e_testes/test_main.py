#testes da API usando TestClient e Pytest
#baseado na documentação: https://fastapi.tiangolo.com/tutorial/testing/

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from model import Produto

#banco separado só pra não bagunçar o estoque.db real
sql_url_teste = "sqlite:///./teste.db"
engine_teste = create_engine(sql_url_teste, connect_args={"check_same_thread": False})
SessionTeste = sessionmaker(autocommit=False, autoflush=False, bind=engine_teste)

Base.metadata.create_all(bind=engine_teste)


def override_get_db():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def limpar_produtos():
    db = SessionTeste()
    db.query(Produto).delete()
    db.commit()
    db.close()


def test_root_status_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Controle de Estoque"}


def test_listar_produtos_status_200():
    limpar_produtos()
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json() == []


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


def test_atualizar_produto_404():
    limpar_produtos()
    response = client.put("/produtos/ProdutoInexistente?quant=1&preco=9.9")
    assert response.status_code == 404
    assert response.json() == {"detail": "Produto não encontrado"}


def test_remover_produto_404():
    limpar_produtos()
    response = client.delete("/produtos/ProdutoInexistente")
    assert response.status_code == 404
    assert response.json() == {"detail": "Produto não encontrado"}


def test_atualizar_e_remover_produto():
    limpar_produtos()

    client.post(
        "/produtos",
        json={"nome": "Caneta", "quantidade": 5, "preco": 2.0},
    )

    response_put = client.put("/produtos/Caneta?quant=8&preco=3.5")
    assert response_put.status_code == 200
    assert response_put.json() == {
        "nome": "Caneta",
        "quantidade": 8,
        "preco": 3.5,
    }

    response_delete = client.delete("/produtos/Caneta")
    assert response_delete.status_code == 200
    assert response_delete.json() == {"message": "Produto removido com sucesso"}
