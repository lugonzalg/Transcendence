from typing import Any, Optional
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
#from ninja.responses import JSONResponse
from ninja.errors import HttpError

from ninja import Router
from . import schemas, crud
from transcendence import Logger

router = Router()
logger = Logger.Logger(name="login")

@router.post('/create_user', response=schemas.UserReturnSchema)
def create_user(request, user: schemas.UserCreateSchema):
    return crud.create_user(user)


@router.get('/get_user')
def get_user(request, user: schemas.Username):

    db_user = crud.get_user(user.username)
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exists")


@router.post('/login_user', response=schemas.UserReturnSchema) #Creacion de endpoint, que especifica el esquema DE RESPUESTA definido en schemas
def login_user(request, user: schemas.UserLogin): #Creacion de funcion que se ejecuta al llamar al endpoint, crea el obj user y lo valida con el schema DE CREACION DE USER definido en schemas

   #llama a la funcion get_user de crud.py y le devuelve el user objeto con la validacion del schema UserLogin
    db_user = crud.get_user(user.username) 
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exist")

    #Comprobacion de contraseña (De momento compara las strings, ya vendra tema HASH)
    if not check_password(user.password, db_user.password):
        raise HttpError(status_code=401, message="Error: incorrect password")

    # Devolver la información del usuario en un diccionario
    return {"username": db_user.username,"email": db_user.email} 



@router.post('/login_log')
def login_log(request, log: schemas.LoginLogSchema):
    logger.info(log)
    return {"test": "ok"}