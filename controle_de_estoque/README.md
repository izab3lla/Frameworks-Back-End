# Controle de Estoque

Projeto de uma API REST para controle de estoque, desenvolvido com Python e FastAPI.

## Como executar

**1. Instale as dependências:**

```bash
pip install fastapi uvicorn
```

**2. Execute o projeto:**

```bash
python -m uvicorn main:app --reload
```

**3. Acesse a documentação no Swagger:**

http://127.0.0.1:8000/docs

## Rotas

- `GET /produtos` — Lista os produtos.
- `POST /produtos` — Cadastra um produto.
- `PUT /produtos/{nome}` — Atualiza um produto.
- `DELETE /produtos/{nome}` — Remove um produto.

## Armazenamento

Os produtos são guardados em uma lista em memória.
