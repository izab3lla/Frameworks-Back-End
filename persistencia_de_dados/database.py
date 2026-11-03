#1 engine - gerencia a conexao entra a aplicacao py e o bd 
#3 session - gerencia a transacao entre a aplicacao py e o bd
#4 get_bd() - cria uma sessao de conexao com o bd e a entrega para quem chamou, depois fecha a sessao
#5 depends - permite que o FastAPI execute uma função automaticamente e disponibilize o resultado para outra função.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

sql_file_name = Path(__file__).resolve().with_name("estoque.db")

#a url aqui vai informar que vai ser usado o sqlite
sql_url = f"sqlite:///{sql_file_name.as_posix()}"

#aqui é uma configuração que vai permitir que o FASTapi e o bd possam compartilhar a conexão 
connection_args = {"check_same_thread": False}

#aqui entra a ultima parte que mantem a conexao disponivel
engine = create_engine(sql_url, connect_args=connection_args)


SessionLocal = sessionmaker(
    autocommit=False, #esse aqui é pra não confirmar as alterações automaticamente
    autoflush=False, #esse pra n enviar as alterações pendentes antes de consulta
    bind=engine #ai esse é pra conectar a sessão ao engine
)

#cria a base para as classes de modelo e assim posso consumir 
#no model.py e criar as tabelas do bd
Base = declarative_base()

def get_db():
    db = SessionLocal() #aqui vai criar uma nova sessão de conexão com o bd
    try:
        yield db #vai entregar a sessão para qm chamou
        #o yield permite que a funções continue depois que a rota terminar
    finally:
        db.close() #aqui fecha e libera os recursos dela, pra n ter sessoões abertas sem necessidade