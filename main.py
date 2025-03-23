from fastapi import FastAPI, Path, Depends, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from jwt_auth import createToken, validateToken
from storage.database import Base, engine, Session
from models.movieModel import Movie as movieModel


app = FastAPI(
    title = "Aprendiendo FastAPI",
    version='0.0.1'
)


Base.metadata.create_all(bind=engine)

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5)
    overview: str
    year: int
    rating: float = Field(ge=1, le=10)
    category: str  


class User(BaseModel):
    email:str
    password: str

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'vago@gmail.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')
        

movies = [ 
        {
            'id': 1,
            'title': "El padrino",
            'overview': "esta guay",
            'year': '1972',
            'rating':9.2,
            'category': 'Crimen'
        }
]

## LOGIN AND SECURITY
oauth = OAuth2PasswordBearer(tokenUrl='token')


@app.post('/login/', tags=["Autenticacion"])
def login(user: User):
    if user.email == 'vago@gmail.com' and user.password == '1234':
        token: str = createToken(user.dict())
        # Use Response with explicit media_type
        return Response(content=f'Welcome, {token}', status_code=200, media_type="text/plain") 
    else:
        return Response(content='Incorrect login', status_code=401, media_type="text/plain") 


@app.get('/movies', tags=['Movies'], dependencies = [Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(movieModel).all()
    return JSONResponse(content=jsonable_encoder(data))


@app.get('/movie', tags=['Movies'], dependencies = [Depends(BearerJWT())])
def get_movie(name: str):
    db = Session()
    data = db.query(movieModel).filter(movieModel.title == name).first()
    if not data:
        return JSONResponse (status_code=404, content={'message':'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category:str):
    db = Session()
    data = db.query(movieModel).filter(movieModel.category == category).all()
    if not data:
        return JSONResponse (status_code=404, content={'message':'Recursos no encontrados'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@app.post('/movies/', tags=['Movies'], status_code=201)
def new_movie(movie: Movie):
    db = Session()
    newMovie = movieModel(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    db.close()
    return JSONResponse(status_code=201, content={'message':'Se ha insertado nueva pelicula', 'movie': '{newMovie.title}'})

@app.put('/movies/{id}', tags=['Movies'], dependencies = [Depends(BearerJWT())])
def update_movie(id:int, movie: Movie):
    db = Session()
    data = db.query(movieModel).filter(movieModel.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'No se encontro el elemento'})
    else:
        data.title=movie.title
        data.overview = movie.overview
        data.year = movie.year
        data.rating = movie.rating
        data.category = movie.category
        db.commit()
        return JSONResponse(content={'message':'Se ha modificado la película'})

@app.delete('/movies/{id}', tags=['Movies'], dependencies = [Depends(BearerJWT())])
def delete_movie(id:int):
    db = Session()
    data = db.query(movieModel).filter(movieModel.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'No se encontro el elemento'})
    else:
        db.delete(data)
        db.commit()
        return JSONResponse(content={'message':'Se ha eliminado la película'})
