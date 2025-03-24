Ejecutar el fichero:
    
    uvicorn main:app --reload

#PyDantic: 
## BaseModel()
Lo que llega a ser una clase en python, se crea y se usa para usar sus atributos
    
    class Movie(BaseModel):
        id: Optional[int] = None
        title: str
        overview: str
        year: int
        rating: float
        category: str

## Field()
Para realizar validaciones, se usa así (en este caso exigimos un minimo de caracteres, tambien se puede poner un default ):
    
    class Movie(BaseModel):
        id: Optional[int] = None
        title: str = Field(defaul='Titulo de la película', min_length=5)
        overview: str
        year: int
        rating: float = Field(ge=1, le=10)
        category: str


## JSONResponse:

ES simple, es para meter la respuesta en un json. 
Ejemplo: 

    @app.post('/movies/', tags=['Movies'])
    def new_movie(movie: Movie):
        movies.append(movie)
        return JSONResponse(content={'Message':'New input done', 'Movie': movie.model_dump_json()})



# Autenticaciones y seguridad
Consta de Header, Payload y Signature. 
## JSON web token (JWT)
>pip install PyJWT

# Database
Usamos SQLAlchemy

    from storage.database import Base, engine, Session

    db = Session()

    data = db.query(modelName).filter(modelName.columnName == value) 

> donde modelName es modelo definido y a la vez tabla de base de datos
> para que el modelo sea tabla en la base de datos, debemos poner lo siguiente al declarar un modelo:

        from storage.database import Base
        from sqlalchemy import Column, Integer, String, Float

        class Movie(Base):
            __tablename__ = 'movies'
            id = Column(Integer, primary_key=True)
            title = Column(String)
            overview = Column (String)
            year = Column(Integer)
            rating = Column(Float)
            category = Column(String)

# Routing
APIRouter

realizando: 

        from fastapi import APIRouter, FastAPI

        app = FastAPI()
        router = APIRouter()

        @router.get('/users', tags=["users"])
        async def read_user():
            return [blablabla]

        app.inclde_router(router)

## DUDA IMPORTANTE, ¿cómo vamos a utilizar todo el tokenizaicon entre dos clases?