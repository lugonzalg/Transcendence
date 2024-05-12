from django.core.validators import validate_email
from ninja.errors import HttpError
from transcendence.settings import JWT, logger
import datetime, jwt
from . import schemas

BEARER_OFFSET = 7
SECRET = JWT['SECRET_KEY']
ALGORITHM = JWT['ALGORITHM']
#REFRESH = JWT['REFRESH']


def encode_token(jwt_input: schemas.JWTInput, exp_time: int = 0) -> str:

    exp_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=jwt_input.expire_time + exp_time)

    payload = {
        "username": jwt_input.username,
        'user_id': jwt_input.user_id,
        "exp": exp_date
    }

    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:

    try:
        decoded = jwt.decode(token, SECRET, algorithms=ALGORITHM)
    except jwt.exceptions.InvalidSignatureError:
        raise HttpError(status_code=401, message="Invalid Token")

    except jwt.exceptions.ExpiredSignatureError:
        raise HttpError(status_code=401, message="Expired Token")

    except jwt.exceptions.DecodeError:
        raise HttpError(status_code=401, message="Bad Token")

    except Exception as err:
        raise HttpError(status_code=401, message="Unhandled Error")

    email = decoded.get("username")
    if email is None:
        raise HttpError(status_code=401, message="Error: User Unauthorized")

    if decoded.get("exp") is None:
        raise HttpError(status_code=401, message="Error: No Time Expedition")

    user_id = decoded.get("user_id")
    if user_id is None:
        raise HttpError(status_code=401, message="Error: no user id")

    return decoded

def create_jwt(username: str, user_id: int):

    jwt_input = schemas.JWTInput(username=username, user_id=user_id)

    #TOKEN
    token = encode_token(jwt_input, 300)

    #REFRESH_TOKEN
    refresh_token = encode_token(jwt_input, 400)

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

def authorize(request):

    auth = request.headers.get("Cookie")
    if auth is None:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    offset = auth.find('Bearer ')
    if offset == -1:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    end = auth.find(';', offset)
    if end == -1:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    auth = auth[offset + 7:end - 1]

    jwt_data = decode_token(auth)
    request.jwt_data = jwt_data

    return request
