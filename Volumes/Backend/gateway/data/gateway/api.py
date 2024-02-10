#CORE

from transcendence.settings import TRANSCENDENCE, logger
from django.http import HttpResponseRedirect

import jwt, datetime, aiohttp
from . import schemas

from ninja import Router
from ninja.errors import HttpError
from django.core.validators import validate_email

router = Router()

BEARER_OFFSET = 7
SECRET = TRANSCENDENCE['JWT']['secret']
ALGORITHM = TRANSCENDENCE['JWT']['algorithm']
REFRESH = TRANSCENDENCE['JWT']['refresh']


def encode_token(jwt_input: schemas.JWTInput) -> str:

    exp_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=jwt_input.expire_time)

    payload = {
        "email": jwt_input.email,
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
        email=email,
        expire_time=30
    )

    jwt_token.token = encode_token(jwt_input)
    return jwt_token

@router.get('/test/login', tags=['test connection'])
async def test_login_connectio(request):

    async with aiohttp.ClientSession() as session:
        async with session.get('http://login:25671/api/login/test') as res:
            return await res.json()

@router.get('/login/google', tags=['login'])
async def login_google(request):

    async with aiohttp.ClientSession() as session:
        async with session.get('http://login:25671/api/login/google') as res:
            payload = await res.json()
            url = payload.get('url')
            if url is None:
                raise HttpError(status_code=400, message="Error: Unknown")

            return HttpResponseRedirect(url)

@router.get('/login/google/callback', tags=['login'])
async def login_google_callback(request):

    async with aiohttp.ClientSession() as session:
        async with session.get('http://login:25671/api/login/google/callback') as res:

            if res.status != 302:
                raise HttpError(status_code=res.status, message="Error: Unknown")

            res = await res.json()
    
    url = res.get('url')
    email = res.get('email')
    jwt_input = schemas.JWTInput(
        email=email,
        expire_time=30
    )
    jwt_token = create_jwt(jwt_input)

    response = HttpResponseRedirect(url)
    response.set_cookie('token', jwt_token.token)
    response.set_cookie('refresh', jwt_token.refresh)
    return response