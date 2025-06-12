from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
O script configura uma conexão com um banco de dados SQLite, cria uma classe de sessão para 
interagir com esse banco e define uma classe base para a criação de modelos de dados. 
É uma configuração comum em aplicações que utilizam SQLAlchemy para gerenciar a persistência de dados.
"""

def get_db():
    """Função que cria uma sessão de banco de dados.

    Returns:
        SessionLocal: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        # Yield em Python é utilizada para criar funções geradoras, que são uma forma 
        # especial de funções que permitem retornar um valor e pausar a execução da 
        # função, mantendo seu estado.
        # Supostamente da próxima vez que esta função é chamada, ela continuará a partir
        # do ponto que parou em vez de reiniciar a execução do código do início.
        yield db
    finally:
        db.close()

SQLARCH_DATABASE_URL = "sqlite:///./product.db"

# Cria uma instancia de conexão com o banco de dados SQLite
engine = create_engine(SQLARCH_DATABASE_URL, connect_args={"check_same_thread": False})

# criando uma sessão local para interações com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos de dados, que será usada para criar tabelas no banco de dados
# A classe base é parte do Object-Relational Mapping (ORM) do SQLAlchemy. Isso significa que ela 
# permite que você trabalhe com objetos Python em vez de interagir diretamente com o banco de 
# dados usando SQL. Você pode criar, ler, atualizar e excluir registros como se estivesse 
# manipulando objetos em Python.
#
# Ao usar uma classe base, você pode facilmente definir relacionamentos entre diferentes 
# tabelas (como um-para-muitos ou muitos-para-muitos) usando as funcionalidades do SQLAlchemy, 
# o que facilita a modelagem de dados complexos.
Base = declarative_base()


