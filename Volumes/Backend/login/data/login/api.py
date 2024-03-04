import hashlib, os , requests, jwt, random, datetime, smtplib
from django.http import HttpResponseRedirect
from urllib.parse import urlencode
from django.contrib.auth.hashers import check_password
#from ninja.responses import JSONResponse
from ninja.errors import HttpError
from django.conf import settings
from django.core.cache import cache
from . import schemas, crud, models
from transcendence.settings import logger, GOOGLE_OUATH, TRANSCENDENCE
#CORE
from django.utils import timezone
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
    return db_user



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
    #headers = {
    #    'Content-Length': '', 'Content-Type': 'text/plain', 'Host': 'localhost:4242', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"macOS"', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.9', 'Cookie': 'grafana_session=ed5c79bc3906813c7b0ffa4fc802fe83'}

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

    #PASO 4 - Filter username info 
    username=user_info.json().get('login')
    email=user_info.json().get('email')

    #PASO 5 - Find if user is in Database
    try:
        db_user = crud.get_user_by_email(email) 
        if db_user.mode != 2: #se puede implementar como variable LOGIN MODE INTRA = 2 
            raise HttpError(status_code=404, message="Error: User already used other authentication method")
        elif check_user(db_user):
            handle_otp(db_user)
            payload['url'] = TRANSCENDENCE['URL']['otp'],
            return 428, payload
        logger.info('EXISTING USER LOGIN OK')
        lobby_url = 'http://localhost:8080/Lobby'
        return {"url":lobby_url} #OK, El usuario ya existe 
    except Exception as err:
        logger.error(err)

    #PASO 6 - Usuario no existe, Create user in Database
    logger.info('Username does not exist, starting creation...')
    user_create_data = {
    "username": username,
    "email": email,
    "password": "IntraIntra42!", #LA ÑAPA DEL SIGLO! Que pasa con la contraseña para los usuarios que acceden por intra?  
    "mode": 2,
    }
    new_user = schemas.UserCreateSchema(**user_create_data)
    db_user = crud.create_user(user=new_user) 

    #COOKIES??

    logger.warning('NEW USER LOGIN OK')
    lobby_url = 'http://localhost:8080/Lobby'
    return {"url": lobby_url}
     

@router.post('/log')
def login_log(request):
    #si meto log: schemas.LoginLogSchema como param no encaja
    logger.warning('DATATOSERVER EN LOGIN/LOG')
    #Se gestionaria esa info, PARA QUE?, Que devolvemos?
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
    logger.warning(user_info)
    try:
        db_user = crud.get_user_by_email(email)
    except Exception as err:
        db_user = None
        logger.error(err)

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