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

