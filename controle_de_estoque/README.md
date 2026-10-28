# Controle de Estoque

API REST desenvolvida com Python e FastAPI para realizar o controle de estoque de produtos.

## Requisitos

Ter o Python instalado no computador.

## Como executar o projeto

**1. Clonar o repositório**

```bash
git clone https://github.com/izab3lla/Frameworks-Back-End/tree/main/controle_de_estoque
```

Entre na pasta do projeto:

```bash
cd controle_de_estoque
```

**2. Instalar as dependências**

```bash
pip install fastapi uvicorn
```

**3. Executar a aplicação**

```bash
python -m uvicorn main:app --reload
```

**4. Acessar a documentação**

Com a aplicação em execução, acesse:

http://127.0.0.1:8000/docs


## Rotas disponíveis

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Exibe uma mensagem inicial |
| GET | `/produtos` | Lista os produtos cadastrados |
| POST | `/produtos` | Cadastra um produto |
| PUT | `/produtos/{nome}` | Atualiza a quantidade e o preço de um produto |
| DELETE | `/produtos/{nome}` | Remove um produto pelo nome |


## Armazenamento dos dados

Os produtos são armazenados em uma lista em memória, sem utilização de banco de dados. Por isso, os dados cadastrados são perdidos quando a aplicação é reiniciada.

