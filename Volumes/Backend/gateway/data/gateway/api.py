#CORE

from transcendence.settings import TRANSCENDENCE, logger
from django.http import HttpResponseRedirect

import hashlib, os, requests, jwt, datetime, aiohttp
from . import schemas

import os
from ninja import Router
from ninja.errors import HttpError
from django.core.validators import validate_email

router = Router()

S_LOGIN_REGISTER= os.environ['S_LOGIN_REGISTER']
S_LOGIN_DEFAULT_LOGIN= os.environ['S_LOGIN_DEFAULT_LOGIN']
S_LOGIN_GOOGLE_LOGIN= os.environ['S_LOGIN_GOOGLE_LOGIN']
S_LOGIN_GOOGLE_CALLBACK= os.environ['S_LOGIN_GOOGLE_CALLBACK']

BEARER_OFFSET = 7
SECRET = TRANSCENDENCE['JWT']['secret']
ALGORITHM = TRANSCENDENCE['JWT']['algorithm']
REFRESH = TRANSCENDENCE['JWT']['refresh']

def encode_token(jwt_input: schemas.JWTInput) -> str:

    exp_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=jwt_input.expire_time)

    payload = {
        "username": jwt_input.username,
        "exp": exp_date
    }

    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:

    try:
        decoded = jwt.decode(token, SECRET, algorithms=ALGORITHM)
    except jwt.exceptions.InvalidSignatureError:
        raise HttpError(status_code=400, message="Error: Invalid Token")

    except jwt.exceptions.ExpiredSignatureError:
        raise HttpError(status_code=403, message="Error: Expired Token")

    except jwt.exceptions.DecodeError:
        raise HttpError(status_code=400, message="Error: Bad Token")

    except Exception as err:
        raise HttpError(status_code=404, message="Error: Unhandled Error")

    email = decode_token.get("email")
    if email is None or not validate_email(email):
        raise HttpError(status_code=403, message="Error: User Unauthorized")

    if decoded.get("exp") is None:
        raise HttpError(status_code=403, message="Error: No Time Expedition")
    return decoded

def create_jwt(jwt_input: schemas.JWTInput):

    #TOKEN
    token = encode_token(jwt_input)

    #REFRESH_TOKEN
    refresh_token = encode_token(jwt_input)

    return schemas.JWTToken(token=token, refresh=refresh_token)

def check_jwt(request, jwt_token: schemas.JWTToken) -> bool | HttpError:

    if not jwt_token.token.startswith("Bearer "):
        raise HttpError(status_code=400, message="Error: Token does not have bearer")

    return decode_token(jwt_token.token[BEARER_OFFSET:])

def refresh_jwt(jwt_token: schemas.JWTToken):

    decoded = decode_token(jwt_token.refresh)

    email = decoded.get("email")
    if email is None:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    jwt_input = schemas.JWTInput(
        username=email,
        expire_time=30
    )

    jwt_token.token = encode_token(jwt_input)
    return jwt_token

#/log se encarga de recibir la informacion recopilada por el servidor sobre el navegador del usuario cuando entra en home y 
# redirigirla al endpoint /log del back para que la gestione. 
@router.post('/log', tags=['log'])
async def log(request):

    logger.warning('DATATOSERVER EN GATEWAY')
    async with aiohttp.ClientSession() as session:
        async with session.post('http://login:25671/api/login/log') as res:
            return await res.json()


@router.get('/test/login', tags=['test connection'])
async def test_login_connectio(request):

    async with aiohttp.ClientSession() as session:
        async with session.get('http://login:25671/api/login/test') as res:
            return await res.json()

@router.get('/login/google', tags=['login'])
def login_google(request):

    state = hashlib.sha256(os.urandom(1024)).hexdigest()
    request.session["google_oauth2_state"] = state

    payload = {"state": state}

    logger.warning(S_LOGIN_GOOGLE_LOGIN)
    res = requests.get(S_LOGIN_GOOGLE_LOGIN, params=payload)

    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")


    if not res.ok:
        detail = info.get('detail')
        if detail is None:
            raise HttpError(status_code=400, message="Error: Unknown error")
        raise HttpError(status_code=res.status_code, message=detail)

    url = info.get('url')
    if url is None:
        raise HttpError(status_code=400, message="Error: url not found")

    return HttpResponseRedirect(url)

@router.get('/login/google/callback', tags=['login'])
def login_google_callback(request, code: str, state: str, error: str | None = None):

    if error:
        raise HttpError(status_code=401, message=f"Error found: {error}")

    user_state = request.session.get('google_oauth2_state')
    if not user_state or state != user_state:
        raise HttpError(status_code=401, message="Error: Unautorithed")
    del request.session['google_oauth2_state']

    params = {
        "code": code,
        "state": state,
    }

    res = requests.get(S_LOGIN_GOOGLE_CALLBACK, params=params)

    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")

    url = info.get('url')
    email = info.get('email')

    #HANDLE OTP
    logger.warning(email)
    logger.warning(info)
    jwt_input = schemas.JWTInput(username=email)

    if not res.ok:
        jwt_input.permission = 0
        jwt_input.expire_time = 5

    jwt_token = create_jwt(jwt_input)
    response = HttpResponseRedirect(url)
    response.set_cookie('token', jwt_token.token)
    response.set_cookie('refresh', jwt_token.refresh)
    return response

@router.get('/otp')
async def check_otp(request):

    """
    jwt_input = schemas.JWTInput(username=email)

    if not res.ok:
        jwt_input.permission = 0
        jwt_input.expire_time = 5

    jwt_token = create_jwt(jwt_input)

    response.set_cookie('token', jwt_token.token)
    response.set_cookie('refresh', jwt_token.refresh)
    """
    return 

@router.get('/intra', tags=['login']) #no entiendo el tema tags 
def login_intra(request):

    #  JWT, OTP y cookies

    res = requests.get('http://login:25671/api/login/intra')
    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")

    if not res.ok:
        detail = info.get('detail')
        if detail is None:
            raise HttpError(status_code=400, message="Error: Unknown error")
        raise HttpError(status_code=res.status_code, message=detail)

    url = info.get('url')
    if url is None:
        raise HttpError(status_code=400, message="Error: url not found")

    return HttpResponseRedirect(url)

@router.get('/login/intra_callback', tags=['login'])
def login_intra_callback(request, code:str):

    payload = {
        "code": code
    }
    res = requests.get('http://login:25671/api/login/intra/callback', params=payload)
    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")

    url = info.get('url')

     # JWT, OTP y cookies

    return HttpResponseRedirect(url)

@router.get('/login/default', tags=['login'])
def login_default(request, username: str, password: str):

    payload = {
        'username': username,
        'password': password
    }
    res = requests.post(S_LOGIN_DEFAULT_LOGIN, json=payload)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message=res.json())

    logger.warning("LOGIN DEFAULT RESULT")
    logger.warning(res.status_code)
    logger.warning(res.json())
    return res.json()

@router.post('/login/register', tags=['login'])
def login_register(request, username: str, email: str, password: str):

    payload = {
        'username': username,
        'password': password,
        'email': email
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    res = requests.post(S_LOGIN_REGISTER, headers=headers, json=payload)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message=res.json())

    return  res.json()

@router.post('/login/unknown', tags=['login'])
def login_unknown(request, username: str):

    jwt_input = schemas.JWTInput(username=username)
    jwt_token = create_jwt(jwt_input)
    return jwt_token