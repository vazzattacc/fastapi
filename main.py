from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI(
    title = "Documentation"
)


movies = [
    'last samurai',
    'ronin',
    'shogun',
    '2 girls one cup'
]
@app.get('/', tags=["inicio"])
def read_root():
    return HTMLResponse('<h1>Hello world!</h1>')


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies


