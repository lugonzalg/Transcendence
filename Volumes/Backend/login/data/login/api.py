from django.contrib.auth.hashers import check_password
from ninja.errors import HttpError

from ninja import Router
from . import schemas, crud
from transcendence.settings import logger, GOOGLE_OUATH

router = Router()

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

import hashlib, os, aiohttp
from django.shortcuts import redirect

@router.post('/google')
async def google_login(request):

    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    
    auth_params = {
    'scope': 'https://www.googleapis.com/auth/drive.metadata.readonly',
    'access_type': 'offline',
    'include_granted_scopes': 'true',
    'response_type': 'code',
    'state': state,
    'redirect_uri': GOOGLE_OUATH['REDIRECT_URI2'],
    'client_id': GOOGLE_OUATH['CLIENT_ID']
    }

    async with aiohttp.ClientSession() as client:
        async with client.get(GOOGLE_OUATH["AUTH_URL"], params=auth_params) as res:

            logger.info(f"URL: {res.url}")
            logger.info(f"PATH: {res.url.raw_path}")
            logger.info(type(res.url))

            return {"url":str(res.url)}

@router.post('/google/callback')
def test(request):
    return {"test": "tset"}