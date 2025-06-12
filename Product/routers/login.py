from fastapi import APIRouter, status, Response, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas, models # .. volta um diretório na hierarquia de pacotes
from ..database import get_db # .. volta um diretório na hierarquia de pacotes
from ..schemas import TokenData
from passlib.context import CryptContext # serve para transformar senhas em hash.
from datetime import datetime, timedelta
from jose import jwt  # biblioteca para manipulação de JWT (JSON Web Tokens)
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

SECRET_KEY = "F752945C26CF8B82790CD18BD9CB3395"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter()

# Contexto de criptografia para senhas, usando bcrypt como algoritmo de hash.
# O bcrypt é um algoritmo de hash seguro e amplamente utilizado para armazenar senhas.
# O bcrypt a ser instalado deve ser a versão 4.0.1 para não dar o warning
# AttributeError: module 'bcrypt' has no attribute '__about__'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

# OAuth2PasswordBearer é uma classe do FastAPI que implementa o fluxo de autenticação OAuth2 com senha.
# Ela é usada para extrair o token de autenticação do cabeçalho Authorization da solicitação HTTP.
# Serve para verificar se o usuário está autenticado antes de acessar rotas protegidas.
# # O tokenUrl é o endpoint onde o usuário pode obter um token de acesso, geralmente após fazer login.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def generate_token(data: dict):
    """
    Função para gerar um token JWT (JSON Web Token) com base nos dados fornecidos.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # gerar o token JWT usando o SECRET_KEY e o ALGORITHM definidos
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Verifica se o usuário existe no banco de dados
    user = db.query(models.Seller).filter(models.Seller.username == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário ou Senha incorreta")
    
    # Verifica se a senha fornecida corresponde à senha armazenada no banco de dados
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou Senha incorreta")
    
    # Gerar topen JWT ou outro mecanismo de autenticação aqui, se necessário.
    token_data = {"username": user.username}
    access_token = generate_token(token_data)

    # Se as credenciais estiverem corretas, retorna uma mensagem de sucesso
    return {"access_token": access_token, "token_type": "bearer", "message": "Login realizado com sucesso"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Função para obter o usuário atual a partir do token JWT.
    """
    try:
        # Decodifica o token JWT usando o SECRET_KEY e o ALGORITHM definidos. Ou seja vai decodificar
        # o token para extrair as informações de usuário logado.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        
        token_data = TokenData(username=username)
        
        return token_data
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

