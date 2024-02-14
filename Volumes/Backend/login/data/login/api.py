from typing import Any, Optional
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
#from ninja.responses import JSONResponse
from ninja.errors import HttpError
import os
import requests
from django.http import HttpResponseRedirect
from django.conf import settings


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
    return db_user

################
# CUSTOM LOGIN #
################

@router.post('/login_user', response=schemas.UserReturnSchema) #Creacion de endpoint, que especifica el esquema DE RESPUESTA definido en schemas
def login_user(request, user: schemas.UserLogin): #Creacion de funcion que se ejecuta al llamar al endpoint, crea el obj user y lo valida con el schema DE CREACION DE USER definido en schemas

   #llama a la funcion get_user de crud.py y le devuelve el user objeto con la validacion del schema UserLogin
    db_user = crud.get_user(user.username) 
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exist")

    #Comprobacion de contraseña (De momento compara las strings, ya vendra tema HASH)
    if not check_password(user.password, db_user.password):
        raise HttpError(status_code=401, message="Error: incorrect password")

     # Devolver la información del usuario (el schema de UserReturnSchema ya filtra lo que devolver, el usuario y el mail en un diccionario
    return {db_user} 

################
# 42 LOGIN #
################

#Construye la URI que se usa para hacer la peticion a la intra.
@router.get('/intra')
def redirect_intra(request): 

    uid = os.environ['INTRA_UID']
    auth_url = os.environ['INTRA_AUTH_URL']
    redirect_uri = os.environ['INTRA_REDIRECT_URI']

    # Construir la URI (la f indica que esta utilizando una cadena de formato f-string en Python.Las expresiones dentro de las llaves se evalúan y se insertan en la cadena resultante.)
    uri = f"{auth_url}?client_id={uid}&redirect_uri={redirect_uri}&response_type=code"

    return ({"url":uri})


@router.get('/intra/callback')
def login_intra(request): 
    
    # PASO 1 - GET CODE 
    # Recibe el código del parámetro GET
    code = request.GET.get('code')
    
    # PASO 2 - INTERCAMBIO DE CODE POR TOKEN 
    # Construye peticion (Credenciales de enviroment, las de la app intra) 
    uid = os.environ.get('INTRA_UID')
    secret = os.environ.get('INTRA_SECRET')
    authorization_url = os.environ.get('INTRA_VERIFY_URL')
    redirect_uri = os.environ.get('INTRA_REDIRECT_URI')
    data = {
        'grant_type': 'authorization_code',
        'client_id': uid,
        'client_secret': secret,
        'code': code,
        'redirect_uri': redirect_uri,
    }
    #Hace un POST para intercambio por TOKEN 
    response=requests.post(os.environ.get('INTRA_VERIFY_URL'), params= data)
    
    if response.status_code != 200:
        raise HttpError(status_code=response.status_code, message="Error: Authentication code Failed")
        return

    #PASO 3 - TOKEN POR INFO (ME)
    #Construye peticion
    access_token = response.json().get('access_token')
    headers = {
    'Authorization': f'Bearer {access_token}'   
    }
    #Hace GET para acceder a la API , endpoint "me"
    user_info = requests.get('https://api.intra.42.fr/v2/me', headers=headers)

    if user_info.status_code != 200:
        raise HttpError(status_code=user_info.status_code, message="Error: Authentication token Failed")
        return

  
    #PASO 4 - Filter username info 
    username=user_info.json().get('login')
    email=user_info.json().get('email')


    #PASO 5 - Find if user is in Database

    db_user = crud.get_user_by_email(email) #igual es mejor buscarlo por email!!!

    if db_user:# El usuario ya existe en la base de datos
        logger.info('EXISTING USER LOGIN OK')
        lobby_url = f'{settings.FRONTEND_BASE_URL}/Lobby'
        return HttpResponseRedirect('http://localhost:8080/Lobby') #OK, El usuario ya existe 

    #PASO 6 - Usuario no existe, Create user in Database
    logger.info('Username does not exist, starting creation...')
    user_create_data = {
    "username": username,
    "email": email,
    "password": "IntraIntra42!", #LA ÑAPA DEL SIGLO! Que pasa con la contraseña para los usuarios que acceden por intra?  
    }
    new_user = schemas.UserCreateSchema(**user_create_data)
    db_user = crud.create_user(user=new_user) 

    #COOKIES??

    logger.info('NEW USER LOGIN OK')
    lobby_url = f'{settings.FRONTEND_BASE_URL}/Lobby'
    return HttpResponseRedirect('http://localhost:8080/Lobby')

        

@router.post('/login_log')
def login_log(request, log: schemas.LoginLogSchema):
    logger.info(log)
    return {"test": "ok"}