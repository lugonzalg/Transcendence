import hashlib, os
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from django.contrib.auth.hashers import check_password
#from ninja.responses import JSONResponse
from ninja.errors import HttpError
from django.core.cache import cache
import random

from . import schemas, crud, models
from transcendence.settings import logger, GOOGLE_OUATH, TRANSCENDENCE

import requests, jwt

#CORE
from ninja import Router

router = Router()

@router.post('/create_user', response=schemas.UserReturnSchema)
def create_user(request, user: schemas.UserCreateSchema):
    return crud.create_user(user, TRANSCENDENCE['LOGIN']['LOCAL'])


@router.get('/get_user')
def get_user(request, user: schemas.Username):

    db_user = crud.get_user(user.username)
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exists")

import datetime, smtplib
from django.utils import timezone


################
# CUSTOM LOGIN #
################

def send_email(sender: str, receiver: str, otp_code: int):

    try:
        mail = schemas.Mail(
            sender=sender,
            receiver=receiver,
        )
    except ValueError as err:
        logger.warning(f"Error: Missing Value(s) {err}")
        return False

    mail.build(otp_code)

    try:
        with smtplib.SMTP(TRANSCENDENCE['SMTP']['address'], TRANSCENDENCE['SMTP']['port']) as server:
            server.sendmail(sender, receiver, mail.message)
        return True

    except Exception as err:
        logger.error(f"Error: Unhandled {err}")

    return False

def handle_otp(db_user: models.user_login) -> bool:

    otp_code=random.randint(0000, 9999)
    cache.add(db_user.username, otp_code, 30)
    return send_email(
        sender=TRANSCENDENCE['SMTP']['sender'],
        receiver=db_user.email,
        otp_code=otp_code
    )

@router.post('/login_user', response={200: schemas.UserReturnSchema, 428: schemas.UserReturnSchema}) #Creacion de endpoint
def login_user(request, user: schemas.UserLogin): #Creacion de funcion que se ejecuta al llamar al endpoint, crea el obj user y lo valida con el schema DE CREACION DE USER definido en schemas

   #llama a la funcion get_user de crud.py y le devuelve el user objeto con la validacion del schema UserLogin
    db_user = crud.get_user(user.username) 
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exist")

    if db_user.mode != TRANSCENDENCE['LOGIN']['LOCAL']:
        raise HttpError(status_code=404, message="Error: User already used other authentication method")

    #Comprobacion de contraseña (De momento compara las strings, ya vendra tema HASH)
    if not check_password(user.password, db_user.password):
        raise HttpError(status_code=401, message="Error: incorrect password")

    if check_user():
        handle_otp()
        return 428, db_user

     # Devolver la información del usuario (el schema de UserReturnSchema ya filtra lo que devolver, el usuario y el mail en un diccionario
    return 200, db_user

############
# 42 LOGIN #
############

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
    
    # Recibe el código del parámetro GET
    code = request.GET.get('code')
     #<QueryDict: {'code': ['5b6f5c362b11172402fd81c8bf4e2f40772bcc6305e0294a4fd763d49643544b']}>

    # Credenciales de la aplicación desde las variables de entorno para construir la peticion de intercambio por token y validar. 
    uid = os.environ.get('INTRA_UID')
    secret = os.environ.get('INTRA_SECRET')
    authorization_url = os.environ.get('INTRA_VERIFY_URL')

    #Construye
    data = {
        'grant_type': 'authorization_code',
        'client_id': uid,
        'client_secret': secret,
        'code': code,
        'redirect_uri': 'tu_uri_de_redireccion',
    }
    #Hace un POST????? ME PIERDOOOOOOOOO
    #request.post()
    # Si en la respuesta esta el token de acceso o no
    #if response.status_code != 200:
        #raiseERror
    #    return response # Devuelve OK al Front

    #token = response.json()['access_token']
    #db_user = crud.create_user(token.username) #userschema   
    

@router.post('/log')
def login_log(request, log: schemas.LoginLogSchema):
    logger.info(log)
    return {"test": "ok"}

@router.post('/test_headers')
def test_headers(request):
    logger.warning("HEADERS")
    logger.warning(request.headers)
    return {"test": "ok"}

################
# GOOGLE LOGIN #
################

@router.get('/google')
def google_login(request, state: str):

    oauth_params = GOOGLE_OUATH['OAUTH_PARAMS_LOGIN']
    oauth_params['scope'] = ' '.join(GOOGLE_OUATH["SCOPES"])
    oauth_params['state'] = state
    oauth_params['redirect_uri'] = GOOGLE_OUATH['REDIRECT_URI']
    oauth_params['client_id'] = GOOGLE_OUATH['CLIENT_ID']

    auth_url = f"{GOOGLE_OUATH['AUTH_URL']}?{urlencode(oauth_params)}"
    return {"url": auth_url}

def check_user(db_user: models.user_login) -> bool:

    last_log = db_user.last_log + datetime.timedelta(minutes=30)
    now = timezone.now()
    db_user.save()

    return now > last_log

@router.get('/google/callback', response={200: dict, 428: dict})
def google_callback(request, code: str, state: str):

    oauth_params = dict(GOOGLE_OUATH['OAUTH_PARAMS_TOKEN'])
    oauth_params['code'] = code
    oauth_params['client_id'] = GOOGLE_OUATH['CLIENT_ID']
    oauth_params['client_secret'] = GOOGLE_OUATH['CLIENT_SECRET']
    oauth_params['redirect_uri'] = GOOGLE_OUATH['REDIRECT_URI']

    res = requests.post(GOOGLE_OUATH['ACCESS_TOKEN_URL'], data=oauth_params)
    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Error: Authentication Failed")

    try:
        google_tokens = res.json()
    except Exception as err:
        raise HttpError(status_code=res.status_code, message="Error: Bad response")

    user_info = jwt.decode(google_tokens['id_token'],options={"verify_signature": False})

    email = user_info.get('email')
    db_user = crud.get_user_by_email(email)

    payload = {
        'url': TRANSCENDENCE['URL']['lobby'],
        'email': email
    }

    if db_user is None:
        logger.warning("User does not exist!")
        new_user = schemas.UserCreateSchema(
            username="place_holder",
            email=email,
            password="Asdfasdfasdf$1"
        )
        crud.create_user(new_user, TRANSCENDENCE['LOGIN']['GOOGLE'])

    elif check_user(db_user):
        handle_otp(db_user)
        payload['url'] = TRANSCENDENCE['URL']['otp'],
        return 428, payload

    return 200, payload

@router.get("/test")
def test_login(request):
    return {"login":"ok"}