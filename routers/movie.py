from fastapi import APIRouter, FastAPI, Path, Depends, HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from jwt_auth import createToken, validateToken
from storage.database import Base, engine, Session
from models.movieModel import Movie as movieModel


movieRouter = APIRouter()


@movieRouter.get('/movies', tags=['Movies'], dependencies = [Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(movieModel).all()
    return JSONResponse(content=jsonable_encoder(data))


@movieRouter.get('/movie', tags=['Movies'], dependencies = [Depends(BearerJWT())])
def get_movie(name: str):
    db = Session()
    data = db.query(movieModel).filter(movieModel.title == name).first()
    if not data:
        return JSONResponse (status_code=404, content={'message':'Recurso no encontrado'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@movieRouter.get('/movies/', tags=['Movies'])
def get_movies_by_category(category:str):
    db = Session()
    data = db.query(movieModel).filter(movieModel.category == category).all()
    if not data:
        return JSONResponse (status_code=404, content={'message':'Recursos no encontrados'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


@movieRouter.post('/movies/', tags=['Movies'], status_code=201)
def new_movie(movie: Movie):
    db = Session()
    newMovie = movieModel(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    db.close()
    return JSONResponse(status_code=201, content={'message':'Se ha insertado nueva pelicula', 'movie': '{newMovie.title}'})

@movieRouter.put('/movies/{id}', tags=['Movies'], dependencies = [Depends(BearerJWT())])
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


@movieRouter.delete('/movies/{id}', tags=['Movies'], dependencies = [Depends(BearerJWT())])
def delete_movie(id:int):
    db = Session()
    data = db.query(movieModel).filter(movieModel.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message':'No se encontro el elemento'})
    else:
        db.delete(data)
        db.commit()
        return JSONResponse(content={'message':'Se ha eliminado la película'})
