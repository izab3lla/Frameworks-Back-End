# Persistência de Dados

API REST desenvolvida com Python e FastAPI para realizar o controle de estoque de produtos. Os dados ficam salvos em um banco SQLite e as migrações são feitas com o Alembic.

## Requisitos

Ter o Python instalado no computador.

## Como executar o projeto

**1. Clonar o repositório**

```bash
git clone https://github.com/izab3lla/Frameworks-Back-End.git
```

Entre na pasta do projeto:

```bash
cd Frameworks-Back-End/persistencia_de_dados
```

**2. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**3. Criar o banco de dados**

```bash
alembic upgrade head
```

Esse comando cria o arquivo `estoque.db` nesta pasta. Ele não é enviado ao GitHub.

**4. Executar a aplicação**

```bash
python -m uvicorn main:app --reload
```

**5. Acessar a documentação**

Com a aplicação em execução, acesse:

http://127.0.0.1:8000/docs

## Rotas disponíveis

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Exibe uma mensagem inicial |
| GET | `/teste-conexao` | Verifica a conexão com o banco |
| GET | `/produtos` | Lista os produtos cadastrados |
| POST | `/produtos` | Cadastra um produto |
| PUT | `/produtos/{nome}` | Atualiza a quantidade e o preço de um produto |
| DELETE | `/produtos/{nome}` | Remove um produto pelo nome |

## Armazenamento dos dados

Os produtos são armazenados no arquivo SQLite `estoque.db`. A pasta `alembic` guarda as migrações do banco. O arquivo `.db` está no `.gitignore` e não sobe para o repositório.
