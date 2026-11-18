#2 - criar as tabelas do bd

from sqlalchemy import Column, Integer, String, Float
from database import Base

#uma classe para criar as tabelas, estou seguindo o que eu tinha colocado no main.py
class Produto(Base):
    __tablename__ = "produtos"

    nome = Column(String, primary_key=True)
    quantidade = Column(Integer)
    preco = Column(Float)

