from fastapi import FastAPI, Path, Depends, HTTPException, Request, Response
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
    return JSONResponse(content=movies)



###  MOVIES LIST ENDPOINTS ###

@app.get('/', tags=["inicio"])
def read_root():
    return HTMLResponse('<h1>Hello world!</h1>')


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id:int = Path(le=100, ge=0)):
    for item in movies:
        if item["id"] == id:
            return item
    return []


@app.get('/movies/', tags=['Movies'])
def get_movies_by_category(category:str):
    for item in movies:
        if item["category"] == category:
            return item
    return category


@app.post('/movies/', tags=['Movies'], status_code=201)
def new_movie(movie: Movie):
    db = Session()
    newMovie = movieModel(**movie.dict())
    db.add(newMovie)
    db.commit()
    db.close()
    return JSONResponse(status_code=201, content={'message':'Se ha insertado nueva pelicula', 'movie': '{newMovie["title"]}'})

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id:int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item['title']=movie.title,
            item['overview'] = movie.overview,
            item['year'] = movie.year,
            item['rating'] = movie.rating,
            item['category'] = movie.category,
            return movies

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
    for item in movies:
        if item['id']==id:
            movies.remove(item)
    return movies


### 

