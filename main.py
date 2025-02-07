from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse


app = FastAPI(
    title = "Documentation"
)


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



@app.get('/', tags=["inicio"])
def read_root():
    return HTMLResponse('<h1>Hello world!</h1>')


@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies


@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id:int):
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
def new_movie(
        id:int = Body(),
        title:str = Body(),
        overview:str = Body(),
        year:str = Body(),
        rating:float = Body(),
        category:str= Body()
    ):
    movie= {
        "id":id,
        "title":title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    }
    movies.append(movie)
    return movies

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(
        id:int, 
        title:str = Body(),
        overview:str = Body(),
        year:str = Body(),
        rating:float = Body(),
        category:str= Body()
        ):
    for item in movies:
        if item["id"] == id:
            item['title']=title,
            item['overview'] = overview,
            item['year'] = year,
            item['rating'] = rating,
            item['category'] = category,
            return movies

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id:int):
    for item in movies:
        if item['id']==id:
            movies.remove(item)
    return movies