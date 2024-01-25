from django.contrib.auth.hashers import check_password
from ninja.errors import HttpError

from ninja import Router
from . import schemas, crud
from transcendence.settings import logger, GOOGLE_OUATH

import requests
import jwt

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
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

@router.get('/google')
def google_login(request):

    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    oauth_params = GOOGLE_OUATH['OAUTH_PARAMS_LOGIN']
    oauth_params['scope'] = ' '.join(GOOGLE_OUATH["SCOPES"])
    oauth_params['state'] = state
    oauth_params['redirect_uri'] = GOOGLE_OUATH['REDIRECT_URI']
    oauth_params['client_id'] = GOOGLE_OUATH['CLIENT_ID']

    request.session["google_oauth2_state"] = state

    logger.info(oauth_params)
    auth_url = f"{GOOGLE_OUATH['AUTH_URL']}?{urlencode(oauth_params)}"
    logger.info(auth_url)
    return HttpResponseRedirect(auth_url)

@router.get('/google/callback')
def google_callback(request, code: str, state: str, error: str | None = None):

    if error:
        raise HttpError(status_code=401, message=f"Error found: {error}")

    user_state = request.session.get('google_oauth2_state')
    if not user_state or state != user_state:
        raise HttpError(status_code=401, message="Error: Unautorithed")
    del request.session['google_oauth2_state']

    oauth_params = GOOGLE_OUATH['OAUTH_PARAMS_TOKEN']
    oauth_params['code'] = code
    oauth_params['client_id'] = GOOGLE_OUATH['CLIENT_ID']
    oauth_params['client_secret'] = GOOGLE_OUATH['CLIENT_SECRET']
    oauth_params['redirect_uri'] = GOOGLE_OUATH['REDIRECT_URI']

    res = requests.post(GOOGLE_OUATH['ACCESS_TOKEN_URL'], data=oauth_params)
    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Error: Authentication Failed")

    google_tokens = res.json()
    user_info = jwt.decode(google_tokens['id_token'],options={"verify_signature": False})
    logger.info(user_info)

    return {"test": "tset"}