from pydantic import BaseModel 

# pra poder retornar no response body das informações do vendedor, sem a senha
class DisplaySeller(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True  # Permite que o Pydantic converta modelos ORM em dicionários

class Product(BaseModel):
    name: str
    price: float
    description: str = None  # Optional field, default is None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sample Product",
                "price": 19.99,
                "description": "This is a sample product description.",
            }
        }

# classe para exibir a saída do produto com o relacionamento com o vendedor.
class DisplayProduct(BaseModel):
    name: str
    price: float
    description: str = None  # Optional field, default is None
    seller: DisplaySeller 

    class Config:
        from_attributes = True # Permite que o Pydantic converta modelos ORM em dicionários

class Seller(BaseModel):
    username: str
    email: str
    password: str


class Login(BaseModel):
    username: str
    password: str 

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None  # Optional field, default is None

    class Config:
        from_attributes = True  # Permite que o Pydantic converta modelos ORM em dicionários