from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, seller, login


app = FastAPI(
    title="Product API",
    version="1.0.0",
    description="API para gerenciar produtos e vendedores desenvolvida a fins de aprendizado.",
    contact={
        "Desenvolvedor": "Lucas Rocha",
        "website": "https://www.linkedin.com/in/lucas-rocha-b8285089/",
        "email": "lrgsps3@gmail.com"
    },
    docs_url="/documentacao"  # URL para acessar a documentação da API
)

app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

# Esta linha vai criar o banco de dados, conectar com ele e criar as tabelas definidas nos modelos.
models.Base.metadata.create_all(bind=engine)



