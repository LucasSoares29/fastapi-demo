from fastapi import APIRouter, status, Response, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .login import get_current_user
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models # .. volta um diretório na hierarquia de pacotes
from ..database import get_db # .. volta um diretório na hierarquia de pacotes

router = APIRouter(
    tags=['Products'],
    prefix="/api/v1/products"  # Prefixo para todas as rotas deste router
)



# Depends(get_db) é um mecanismo do FastAPI que permite injetar dependências em rotas.
# ou seja, é uma função depende de outra função para retornar um determinado valor.

# código 201 indica que uma nova linha foi criada com sucesso no banco de dados.
@router.post("/addProduct", status_code=status.HTTP_201_CREATED)
def add_product(seller_id: int, request: schemas.Product, db: Session = Depends(get_db)):
    """Função que adiciona um novo produto.

    Args:
        request (schemas.Product): Produto a ser adicionado

    Returns:
        dict: Mensagem de confirmação com os detalhes do produto adicionado
    """
    seller = db.query(models.Seller).filter(models.Seller.id == seller_id).first()
    if seller is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Vendedor não encontrado")

    new_product = models.Product(
        name=request.name,
        price=request.price,
        description=request.description,
        seller_id=seller_id
    )

    db.add(new_product) # inserindo novo produto na sessão do banco de dados
    db.commit() # confirmando a transação
    db.refresh(new_product) # salvando o novo produto no banco de dados e atualizando o objeto na sessão
    return {"message": "Product added successfully", "product": request}

@router.get("/listAllProducts", response_model=List[schemas.DisplayProduct])
def list_all_products(db: Session = Depends(get_db)):
    """Função que retorna todos os produtos.

    Args:
        db (Session, optional): Sessão do banco de dados. Defaults to Depends(get_db).

    Returns:
        list: Lista de produtos
    """
    products = db.query(models.Product).all()
    return products

@router.get("/getProduct/{product_id}", response_model=schemas.DisplayProduct)
def get_product(product_id: int, db: Session = Depends(get_db), response: Response = None):
    """Função que retorna um produto específico pelo ID.

    Args:
        product_id (int): ID do produto a ser retornado
        db (Session, optional): Sessão do banco de dados. Defaults to Depends(get_db).

    Returns:
        Product: Produto encontrado ou None se não encontrado
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Produto não encontrado")
        
    return product

@router.delete("/deleteProduct/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: schemas.Seller = Depends(get_current_user)):
    """Função que deleta um produto pelo ID.

    Args:
        product_id (int): ID do produto a ser deletado
        db (Session, optional): Sessão do banco de dados. Defaults to Depends(get_db).

    Returns:
    """

    # O syncronize_session=False é usado para evitar que o SQLAlchemy sincronize a sessão atual com o banco de dados.
    # Isso é útil quando você está fazendo uma operação de exclusão e não precisa que a sessão atual seja atualizada imediatamente.
    # Isso pode melhorar o desempenho, especialmente em operações de exclusão em massa.
    # Mas se você quiser que a sessão atual seja atualizada imediatamente após a exclusão, você pode usar synchronize_session=True.
    if current_user.username == "admin":
        db.query(models.Product).filter(models.Product.id == product_id).delete(synchronize_session=False)
        db.commit()
        return {"message": "Produto deletado com sucesso", "product_id": product_id}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Acesso negado. Apenas administradores podem excluir produtos.")

@router.put("/updateProduct/{product_id}")
def update_product(product_id: int, request: schemas.Product, db: Session = Depends(get_db)):
    """Função que atualiza um produto pelo ID.

    Args:
        product_id (int): ID do produto a ser atualizado
        request (schemas.Product): Dados do produto a serem atualizados
        db (Session, optional): Sessão do banco de dados. Defaults to Depends(get_db).

    Returns:
        dict: Mensagem de confirmação com os detalhes do produto atualizado
    """
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        return {"message": "Produto não encontrado", "product_id": product_id}

    # Atualizando os campos do produto com os dados do request
    product.name = request.name
    product.price = request.price
    product.description = request.description
    product.seller_id = request.seller_id if hasattr(request, 'seller_id') else product.seller_id 

    db.commit()
    db.refresh(product)
    
    return {"message": "Produto atualizado com sucesso", "product": product}


