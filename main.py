from fastapi import FastAPI, Body, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from jwt import createToken


app = FastAPI(
    title = "Aprendiendo FastAPI"
    version='0.0.1'
)


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


@app.post('/login/', tags=["Autenticacion"])
def login(user: User):
    return user


@app.get('/', tags=["inicio"])
def read_root():
    return HTMLResponse('<h1>Hello world!</h1>')


@app.get('/movies', tags=['Movies'])
def get_movies():
    return JSONResponse(content=movies)


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



@app.post('/movies/', tags=['Movies'])
def new_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={'Message':'New input done', 'Movie': movie.model_dump_json()})



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


