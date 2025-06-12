# Este arquivo serve para criar a tabela de produtos no banco de dados usando SQLAlchemy.

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


# atua como um modelo de dados para a tabela de produtos para criar a tabela sem saber uma linha de SQL
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    seller_id = Column(Integer, ForeignKey('sellers.id'))  # Relacionamento com a tabela de vendedores 
    seller = relationship("Seller", back_populates="products")  # Define o relacionamento com Seller

# assim que você salva models.py com uma nova classe, lá no banco de dados é criado uma nova tabela.
class Seller(Base):
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Senha deve ser armazenada de forma segura
    products = relationship("Product", back_populates="seller")  # Define o relacionamento com Product