from fastapi import FastAPI, Path, Depends, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from jwt_auth import createToken, validateToken
from storage.database import Base, engine, Session
from models.movieModel import Movie as movieModel
from routers.movie import movieRouter

app = FastAPI(
    title = "Aprendiendo FastAPI",
    version='0.0.1'
)

app.include_router(movieRouter)

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

