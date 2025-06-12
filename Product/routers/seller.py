from fastapi import APIRouter, status, Response, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas, models # .. volta um diretório na hierarquia de pacotes
from ..database import get_db # .. volta um diretório na hierarquia de pacotes
from passlib.context import CryptContext # serve para transformar senhas em hash.

router = APIRouter(
    tags=['Sellers'],
    prefix="/api/v1/sellers"  # Prefixo para todas as rotas deste router
)

# Contexto de criptografia para senhas, usando bcrypt como algoritmo de hash.
# O bcrypt é um algoritmo de hash seguro e amplamente utilizado para armazenar senhas.
# O bcrypt a ser instalado deve ser a versão 4.0.1 para não dar o warning
# AttributeError: module 'bcrypt' has no attribute '__about__'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  

# O response_model é usado para especificar o modelo de resposta que será retornado pela rota.
# Com isso consigo configurar para que ele não retorne a senha descriptografada no response_body.
@router.post("/addNewSeller", status_code=status.HTTP_201_CREATED)
def add_new_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    """Função que cria um novo vendedor.

    Args:
        request (schemas.Seller): Dados do vendedor a ser criado
        db (Session, optional): Sessão do banco de dados. Defaults to Depends(get_db).

    Returns:
        dict: Mensagem de confirmação com os detalhes do vendedor criado
    """

    # Aqui estamos usando o CryptContext para hashear a senha do vendedor antes de armazená-la no banco de dados.
    # O hash é uma representação criptográfica da senha, que é mais segura do que armazenar a senha em texto simples.
    hashed_password = pwd_context.hash(request.password)

    new_seller = models.Seller(
        username=request.username,
        email=request.email,
        password=hashed_password
    )

    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)

    output_seller = schemas.DisplaySeller(
        username=new_seller.username,
        email=new_seller.email
    )
    
    return {"message": "Vendedor criado com sucesso", "seller": output_seller}