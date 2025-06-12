from fastapi import FastAPI, Form
from pydantic import BaseModel, Field, HttpUrl
from typing import Set, List
from datetime import datetime

# A documentação do FastAPI é gerada automaticamente
# e pode ser acessada em http://localhost:8000/docs
# ou através do Swagger UI em http://localhost:8000/redoc


# Importando o Pydantic para  definir os modelos de dados para montar o Request Body 
# para ser utilizado em requisições HTTP POST ou PUT para inserir ou atualizar dados.
# O campo Field serve para fornecer metadados adicionais para o campo do modelo, 
# util para o desenvolver conseguir entender os campos que devem ser preenchidos no request body.


# A classe Thumbnail representa uma miniatura de filme, contendo um campo URL.
# Foi criada para demonstrar como usar uma classe dentro de outra classe no Pydantic. 
class Thumbnail(BaseModel):
    url: HttpUrl = Field(title="URL da Miniatura",
                        description="URL da miniatura do filme, deve ser uma URL válida",
                        example="https://example.com/thumbnail.jpg")
    

class Movie(BaseModel):
    name: str = Field(title="Título do Filme", 
                      description="Nome do filme a ser inserido")
    year: int = Field(title="Ano do Filme", 
                      description="Ano de lançamento do filme a ser inserido",
                      gt=1900,
                      lt=2100) # gt: greater than, lt: less than
    tags: Set[str] = Field(default_factory=set,
                           title="Tags do Filme",
                           description="Conjunto de tags associadas ao filme, como gênero ou tema",
                           example=["Sci-Fi", "Adventure"])  # # Set é utilizado para evitar duplicatas nas tags
    thumbnail: List[Thumbnail] = Field(default_factory=list,   
                                         title="Miniaturas do Filme",
                                         description="Lista de miniaturas associadas ao filme, cada uma com uma URL válida",
                                         example=[{"url": "https://example.com/thumbnail1.jpg"},
                                                  {"url": "https://example.com/thumbnail2.jpg"}])
    created_at: datetime = Field(default_factory=datetime.now,
                                 title="Data de Criação",
                                 description="Data e hora em que o filme foi cadastrado",
                                 example="2023-10-01T12:00:00Z")  # Exemplo de data no formato ISO 8601
    
    # Fornecendo exemplo de como o modelo deve ser preenchido na documentação do FastAPI.
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Titanic",
                "year": 1997,
                "tags": ["Drama", "Romance"],
                "thumbnail": [{"url": "https://example.com/titanic_1.jpg"},
                              {"url": "https://example.com/titanic_2.jpg"},
                              {"url": "https://example.com/titanic_3.jpg"}],
                "created_at": "2023-10-01T12:00:00Z"
            }
        }


# Dicionário de filmes para simular um banco de dados
dict_movies = {
    1: {'name': 'Back to The Future', 
        'year': 1985, 
        'tags': ['Sci-Fi', 'Adventure'], 
        'thumbnail': [Thumbnail(url='https://example.com/back_to_the_future.jpg'), 
                      Thumbnail(url='https://example.com/back_to_the_future2.jpg')],
        'created_at': datetime(2023, 10, 1, 12, 0, 0)},
    2: {'name': 'Cars', 
        'year': 2006, 
        'tags': ['Animation', 'Family'], 
        'thumbnail': Thumbnail(url='https://example.com/cars.jpg'),
        'created_at': datetime(2023, 10, 1, 12, 0, 2)},
    3: {'name': 'Transformers', 
        'year': 2007, 
        'tags': ['Action', 'Sci-Fi'], 
        'thumbnail': Thumbnail(url='https://example.com/transformers.jpg'),
        'created_at': datetime(2023, 10, 1, 12, 0, 5)},
    4: {'name': 'The Matrix', 
        'year': 1999, 
        'tags': ['Sci-Fi', 'Action'], 
        'thumbnail': Thumbnail(url='https://example.com/the_matrix.jpg'),
        'created_at': datetime(2023, 10, 1, 12, 0, 9)},
    5: {'name': 'The Lord of the Rings', 
        'year': 2001, 
        'tags': ['Fantasy', 'Adventure'], 
        'thumbnail': Thumbnail(url='https://example.com/lord_of_the_rings.jpg'),
        'created_at': datetime(2023, 10, 1, 12, 0, 11)},
    6: {'name': 'Mickey 17', 
        'year': 2025, 
        'tags': ['Sci-Fi', 'Adventure'], 
        'thumbnail': Thumbnail(url='https://example.com/mickey_17.jpg'),
        'created_at': datetime(2023, 10, 1, 12, 0, 16)}
}


app = FastAPI()


## Criação de endpoints para executar funções no fast api
## Faz a ligação da URL com a função.
@app.get("/")
def index():
    return 'Hello, World!'

@app.get("/movies")
def get_movies(id: int = 0):
    """Retorna as informações com os filmes. Passando o ID do filme igual a 0, retorna todos os filmes.
    
    Args:
        id (int): ID do filme desejado

    Returns:
        dict: Informações do filme ou mensagem de erro

    Example:
        /movies?id=1
    
    """
    if id == 0:
        return dict_movies
    
    return dict_movies.get(id, {'error': 'Movie not found'})

@app.post("/insert_movie")
def insert_movie(movie: Movie):
    """Insere um novo filme no dicionário de filmes.
    
    Args:
        movie (Movie): Objeto do tipo Movie contendo as informações do filme

    Returns:
        dict: Mensagem de sucesso ou erro

    Example:
        /insert_movie
        {
            "name": "New Movie",
            "year": 2023,
            "tags": ["Drama", "Thriller"],
            "thumbnail": [{"url": "https://example.com/new_movie.jpg"}]
        }
    """

    new_id = len(dict_movies) + 1
    dict_movies[new_id] = movie.model_dump()
    dict_movies[new_id]['created_at'] = datetime.now()
    dict_movies[new_id]['modified_at'] = None  # Inicialmente, não há modificação

    # Retorna uma mensagem de sucesso com o ID do novo filme    
    return {'message': 'Filme cadastrado com sucesso', 
            'id': new_id,
            'name': dict_movies[new_id].get('name'),
            'year': dict_movies[new_id].get('year'),
            'tags': dict_movies[new_id].get('tags'),
            'thumbnail': [thumb.get('url', 'Não informado') for thumb in dict_movies[new_id].get('thumbnail', [])],
            'created_at': dict_movies[new_id].get('created_at').isoformat() if dict_movies[new_id].get('created_at') else 'Não informado',
            'modified_at': dict_movies[new_id].get('modified_at').isoformat() if dict_movies[new_id].get('modified_at') else 'Não informado'
            }


@app.post("/insert_thumbnail")
def insert_thumbnail(id: int = Form(...), 
                     url: HttpUrl = Form(...)):
    """Insere uma nova miniatura para um filme existente.
    
    Args:
        id (int): ID do filme ao qual a miniatura será adicionada
        url (HttpUrl): URL da miniatura a ser adicionada

    Returns:
        dict: Mensagem de sucesso ou erro

    Example:
        /insert_thumbnail?id=1&url=https://example.com/new_thumbnail.jpg
    """
    if id not in dict_movies:
        return {'error': 'Movie not found'}
    
    new_thumbnail = Thumbnail(url=url)

    if isinstance(dict_movies[id]['thumbnail'], list):
        # Se for uma lista, adiciona a lista já existente
        dict_movies[id]['thumbnail'].append(new_thumbnail)
    else:
        # Se não, vai ser uma nova lista
        dict_movies[id]['thumbnail'] = [dict_movies[id]['thumbnail'], new_thumbnail]
    
    dict_movies[id]['modified_at'] = datetime.now()
    
    return {'message': 'Miniatura adicionada com sucesso', 
            'movie_id': id, 
            'thumbnail_url': new_thumbnail.url}

