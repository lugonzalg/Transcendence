from typing import Any, Optional
from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
#from ninja.responses import JSONResponse
from ninja.errors import HttpError
import os
import requests

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

     # Devolver la información del usuario (el schema de UserReturnSchema ya filtra lo que devolver, el usuario y el mail en un diccionario
    return {db_user} 


@router.get('/intra')
def redirect_intra(request): #Construye la URI que se usa para hacer la peticion a la intra 

    #esta metida como un churro, como metemos las variables client_id, redirect_uri, ...?  
    #Si la url es siempre igual loguee quien se loguee, igual no es necesario este endpoint?
    peticion = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-6b7efca18b23485e50a6d9bc6df43ecc1024f25f5cf92dc6fd473fcc8647e21c&redirect_uri=http%3A%2F%2Flocalhost%3A25671%2Fapi%2Flogin%2Fintra%2Fcallback&response_type=code"

    uid = os.environ['INTRA_UID']
    auth_url = os.environ['INTRA_AUTH_URL']
    redirect_uri = ['INTRA_REDIRECT_URI']

    # Construir la URI (la f indica que esta utilizando una cadena de formato f-string en Python.Las expresiones dentro de las llaves se evalúan y se insertan en la cadena resultante.)
    uri = f"{auth_url}?client_id={uid}&redirect_uri={redirect_uri}&response_type=code"

    return ({"url":uri})


@router.get('/intra/callback')
def login_intra(request): 
    
    # PASO 1 - GET CODE 
    # Recibe el código del parámetro GET
    code = request.GET.get('code')
     #<QueryDict: {'code': ['5b6f5c362b11172402fd81c8bf4e2f40772bcc6305e0294a4fd763d49643544b']}>
    logger.info('PASO 1 CODE')
    logger.info(code)
    
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
        logger.error('PASO 2 ERROR - code no valido')
        return
    logger.info('PASO 2 TOKEN')
    logger.info(response.json().get('access_token'))

    #PASO 3 - TOKEN POR INFO (ME)
    #Construye peticion
    access_token = response.json().get('access_token')
    headers = {
    'Authorization': f'Bearer {access_token}'   
    }
    #Hace GET para acceder a la API , endpoint "me"
    user_info= requests.get('https://api.intra.42.fr/v2/me', headers)
    

    if user_info.status_code != 200:
        logger.error('PASO 3 ERROR - token no valido')
        return
        #raiseERror
    logger.info('PASO 3 INFO USER')
    logger.info(user_info.json())
  
    #PASO 4 - Username from 
    username=response.get('login')
    logger.info('PASO 4 USERNAME')
    logger.info(user_info.json())
   # logger.info(username)

    #PASO 5 - Create user 
    #token = response.json()['access_token']
    #db_user = crud.create_user(token.username) #userschema   

    logger.info('POST OK')
    return #response # Devuelve OK al Front, pero no la response, otro tipo 
        
    

@router.post('/login_log')
def login_log(request, log: schemas.LoginLogSchema):
    logger.info(log)
    return {"test": "ok"}