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