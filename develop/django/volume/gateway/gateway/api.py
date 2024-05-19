#CORE

from transcendence.settings import logger, GOOGLE
from django.http import HttpResponseRedirect

import hashlib, os, requests
from . import schemas, auth
from typing import Optional

import os
from ninja import Router, UploadedFile, File
from ninja.errors import HttpError

router = Router()

logger.warning(GOOGLE)
S_LOGIN_REGISTER= GOOGLE["LOGIN_GOOGLE"]['S_LOGIN_REGISTER']
S_LOGIN_DEFAULT_LOGIN= GOOGLE["LOGIN_GOOGLE"]['S_LOGIN_DEFAULT_LOGIN']
S_LOGIN_GOOGLE_LOGIN= GOOGLE["LOGIN_GOOGLE"]['S_LOGIN_GOOGLE_LOGIN']
S_LOGIN_GOOGLE_CALLBACK= GOOGLE["LOGIN_GOOGLE"]['S_LOGIN_GOOGLE_CALLBACK']

#/log se encarga de recibir la informacion recopilada por el servidor sobre el navegador del usuario cuando entra en home y 
# redirigirla al endpoint /log del back para que la gestione. 
@router.post('/log', tags=['log'])
async def log(request):

    logger.warning('DATATOSERVER EN GATEWAY')
    return {"msg": 1}


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

    return {'url':url}

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

    logger.warning(f"Params: {params}")
    res = requests.get(S_LOGIN_GOOGLE_CALLBACK, params=params)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Login Service Failed")

    try:
        info = res.json()
    except Exception as err:
        raise HttpError(status_code=500, message="Error: Login Service Failed")

    url = info.get('url')
    username = info.get('username')
    user_id = info.get('user_id')

    #HANDLE OTP
    logger.warning(f"EMAIL: {username}")
    logger.warning(info)
    jwt_input = auth.create_jwt(username=username, user_id=user_id)

    response = HttpResponseRedirect(url)
    response.set_cookie('Authorization', f"Bearer {jwt_input.token}")
    response.set_cookie('Refresh', jwt_input.refresh)
    logger.warning(f"Send token: {jwt_input.token}")
    return response

@router.post('/test_otp')
def test_otp(request, receiver: str):

    payload = {"receiver": receiver}

    res = requests.post("http://login:25671/api/login/test/otp", params=payload)
    return res.json()

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

    username=info.get("username")
    user_id=info.get("user_id")
    url=info.get("url")

    jwt_input = auth.create_jwt(username=username, user_id=user_id)

    response = HttpResponseRedirect(url)
    response.set_cookie('Authorization', f"Bearer {jwt_input.token}")
    response.set_cookie('Refresh', jwt_input.refresh)
    logger.warning(f"Send token: {jwt_input.token}")

    return response

@router.post('/login/default', tags=['login'])
def login_default(request, user: schemas.UserLogin):

    res = requests.post(S_LOGIN_DEFAULT_LOGIN, json=user.__dict__)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Error: Login failed")

    info = res.json()
    user_id = info.get('id')
    username = info.get('username')
    logger.warning(info)
    jwt_input =  auth.create_jwt(username=username, user_id=user_id)

    response = HttpResponseRedirect('https://www.ikerketa.com/dashboard')
    response.set_cookie('Authorization', f"Bearer {jwt_input.token}")
    response.set_cookie('Refresh', jwt_input.refresh)
    return response

@router.post('/login/register', tags=['login'])
def login_register(request, user: schemas.UserRegister):

    payload = {
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'mode': 0
    }

    logger.warning(S_LOGIN_REGISTER)
    res = requests.post(S_LOGIN_REGISTER, json=payload)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Error: Register failed")

    info = res.json()
    logger.warning(info)
    user_id = info.get('user_id')
    username = info.get('username')
    url = info.get("url")

    jwt_input = auth.create_jwt(username=username, user_id=user_id)

    #response.set_cookie('Authorization', f"Bearer {jwt_input.token}")
    #response.set_cookie('Refresh', jwt_input.refresh)
    logger.warning(f"Send token: {jwt_input.token}")

    return url

#@router.post('/login/unknown', tags=['login'])
#def login_unknown(request, username: str):
#
#    jwt_token = auth.create_jwt(username, -1)
#    return jwt_token

@router.get("/middleware", auth=auth.authorize)
def test_middleware(request):
    return {"msg": 1}

#########
#  JWT  #
#########

@router.get('/refresh', tags=['jwt'])
def refresh_token(request):

    logger.warning(request.headers)
    return


############
#   USER   #
############

@router.post('/user/add/friend', auth=auth.authorize, tags=['user'])
def add_friend(request, friendname: str):

    payload = {
        'user_id': request.jwt_data.get('user_id'),
        'friendname': friendname
    }

    logger.warning(payload)
    res = requests.post('http://user:22748/api/user/add/friend', params=payload)

    if not res.ok:
        logger.error(res.json())
        raise HttpError(message='Error: Adding Friend', status_code=res.status_code)

    logger.warning(f"JWT DATA: {request.jwt_data}")
    return {"msg": 1}

@router.delete('/user/delete/friend', auth=auth.authorize, tags=['user'])
def add_friend(request, friendname: str):

    payload = {
        'user_id': request.jwt_data.get('user_id'),
        'friendname': friendname
    }

    logger.warning(payload)
    res = requests.delete('http://user:22748/api/user/delete/friend', params=payload)

    if not res.ok:
        logger.error(res.json())
        raise HttpError(message='Error: Deleting Friend', status_code=res.status_code)

    return {"msg": 1}

@router.post('/user/profile', tags=['user'], auth=auth.authorize)
def update_profile(request, user_profile: schemas.UserProfile, image: File[UploadedFile]):

    logger.warning(image.name)
    user_id = request.jwt_data.get('user_id')
    files = {
        'image': (image.field_name, image.file, image.content_type)
    }
    payload = {
        'user_id': user_id,
        'username': user_profile.username,
        'email': user_profile.email,
        'bio': user_profile.bio
    }
    res = requests.post('http://user:22748/api/user/profile', params=payload, files=files)

    if not res.ok:
        logger.error(res.json())
        raise HttpError(status_code=res.status_code, message="Profile update failed")

    return {'message': 'success'}

@router.get('/user/profile', auth=auth.authorize, tags=['user'])
def get_profile(request):

    logger.warning('Get profile data')
    user_id = request.jwt_data.get('user_id')

    res = requests.get('http://user:22748/api/user/profile', params={'user_id': user_id})

    if not res.ok:
        raise HttpError(status_code=res.status_code, message='Fetching user data failed')

    return res.json()


@router.get('/user/friend/list', auth=auth.authorize, tags=['user'])
def get_profile(request):

    payload = {
        'user_id': request.jwt_data.get('user_id')
    }

    res = requests.get('http://user:22748/api/user/friend/list', params=payload)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message="Failed fetching user friend list")

    return res.json()

@router.delete('/delete/lukas')
def delete_lukas(request):

    requests.delete('http://user:22748/api/user/delete/lukas')
    return {'msg': 1}

@router.post('/user/add', auth=auth.authorize, tags=['user'])
def search_user(request, user: schemas.User):

    payload = {
        'user_id': int(request.jwt_data.get('user_id')),
        'username': request.jwt_data.get('username'),
        'friendname': user.username
    }

    res = requests.post('http://user:22748/api/user/add', params=payload)

    info = res.json()

    if not res.ok:
        raise HttpError(status_code=res.status_code, message=info.get('detail', 'Empty'))

    return res.json()

@router.post('/auth')
def auth_user(request, jwt: str) -> int:

    offset = jwt.find('Bearer ')
    if offset == -1:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    end = jwt.find(';', offset)
    if end == -1:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    jwt = jwt[offset + 7:end - 1]

    jwt_data = auth.decode_token(jwt)
    return jwt_data

@router.post('/user/friend/request', auth=auth.authorize, tags=['user'])
def friend_request(request, friend: schemas.FriendRequest):

    payload = {
        'status': friend.status,
        'user_id' : request.jwt_data.get('user_id'),
        'friend_id' : friend.id
    }

    res = requests.post('http://user:22748/api/user/friend/request', params=payload)

    if not res.ok:
        raise HttpError(status_code=res.status_code, message='test')

    return res.json()

########
# GAME #
########

def safe_post(context: str, url: str, params: dict = None, json: dict = None) -> Optional[object]:

    try:
        res = requests.post(url, params=params, json=json)

        return res
    except Exception as err:
        logger.error(f'Exception for {context}: {err}')

    return None

@router.post('/user/challenge', auth=auth.authorize)
def new_game(request, simple: schemas.SimpleRequest):

    user_id = request.jwt_data.get('user_id')

    payload = {
        'user_id': user_id,
        'friend_id': simple.id
    }
    
    res = safe_post('create challenge', 'http://user:22748/api/user/challenge', params=payload)

    if not res.ok:
        raise HttpError(status_code=409, message='Challenge failed')

    return res.json()

@router.post('/user/challenge/response', auth=auth.authorize)
def challenge_response(request, challenge: schemas.ChallengeResponse):

    payload = {
        'user_id': request.jwt_data.get('user_id'),
        'friend_id': challenge.id,
        'response': challenge.response
    }

    res = safe_post('challenge response', 'http://user:22748/api/user/challenge/response', params=payload)

    if not res or not res.ok:
        raise HttpError(status_code=409, message='Challenge response failed')

    return res.json()

@router.get('/test_ws')
def test_ws(request):

    res = requests.get('http://user:22748/api/user/ws')

    logger.warning(f"test res: {res.status_code}")

    return {"msg": 1}

def safe_get(url: str, params: dict = None) -> Optional[object]:

    try:
        res = requests.get(url, params)
        return res
    except Exception as err:
        logger.error(err)
    return None

##########
#  GAME  #
##########

@router.get('/game/ok', tags=['game'])
def game_service_ok(request):

    res = safe_get('http://game:7777/api/game/ok')

    if res is None or not res.ok:
        raise HttpError(status_code=400, message="game service failed")

    return {"message":"game service up"}

@router.post('/game/create', tags=['game'])
def create_game(request):

    res = safe_post('create game', 'http://game:7777/api/game/create')

    if res is None or not res.ok:
        if res:
            logger.error(f"status: {res.status_code} - detail: {res.json()}")

        raise HttpError(status_code=400, message="match create failed")

    return {'message': 'match created succesfully'}

@router.get('/game/start', auth=auth.authorize, tags=['game'])
def start_match(request):

    params = {
        'user_id': request.jwt_data.get('user_id')
    }

    res = safe_get('http://game:7777/api/game/start', params=params)

    if res is None or not res.ok:
        raise HttpError(status_code=404, message='game start failed')

    return {'message': 'start ok'}

LEFT = False
RIGHT = True

@router.get('/game/left', auth=auth.authorize)
def move_pad_left(request):

    params = {
        'user_id': request.jwt_data.get('user_id'),
        'direction': LEFT
    }

    res = safe_get('http://game:7777/api/game/move', params=params)

    return {'message': 'moved'}

@router.get('/game/right', auth=auth.authorize)
def move_pad_left(request):

    params = {
        'user_id': request.jwt_data.get('user_id'),
        'direction': RIGHT
    }

    res = safe_get('http://game:7777/api/game/move', params=params)

    return {'message': 'moved'}

@router.get('/game/echo')
def game_echo(request):

    res = safe_get('http://game:7777/api/game/echo')

    return {'message': "ok"}