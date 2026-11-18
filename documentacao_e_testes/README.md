# Documentação e Testes

API REST desenvolvida com Python e FastAPI para controle de estoque. Nesta atividade foquei em melhorar a documentação do Swagger e criar testes automatizados com Pytest e TestClient.

## Requisitos

Ter o Python instalado no computador.

## Como executar o projeto

**1. Clonar o repositório**

```bash
git clone https://github.com/izab3lla/Frameworks-Back-End.git
```

Entre na pasta do projeto:

```bash
cd Frameworks-Back-End/documentacao_e_testes
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

No Swagger dá pra ver as tags, os títulos, as descrições e as respostas de cada rota.

## Como rodar os testes

Ainda dentro da pasta `documentacao_e_testes`:

```bash
pytest
```

Se quiser ver o nome de cada teste:

```bash
pytest -v
```

Os testes usam o `TestClient` do FastAPI junto com o Pytest. Eles rodam em um banco separado (`teste.db`), então o `estoque.db` não é alterado.

Tem testes de status 200, cadastro de produto, erro 404 na atualização e na remoção, e também um teste do fluxo completo.

## Armazenamento dos dados

Os produtos são armazenados no arquivo SQLite `estoque.db`. A pasta `alembic` guarda as migrações do banco. O arquivo `.db` está no `.gitignore` e não sobe para o repositório.
