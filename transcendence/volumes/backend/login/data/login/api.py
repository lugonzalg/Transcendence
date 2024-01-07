from typing import Any, Optional
from django.http import HttpRequest
from ninja.security import HttpBearer
from ninja import Router
from . import schemas, crud
import logging

logger = logging.getLogger(__name__)

router = Router()

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post('/create_user', response=schemas.UserReturnSchema)
def create_user(request, user: schemas.UserCreateSchema):

    hashed_password = get_password_hash(user.password)

    return crud.create_user(user, hashed_password)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(login: str, password: str):
    user = crud.get_user(login)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

class Authentication(HttpBearer):

    def authenticate(self, request, token):
        logger.warning(f"Token: {token}")
        if token == "supersecret":
            return token


@router.get('/get_user', auth=Authentication())
def get_user(request, user: str):
    pass

@router.get('/bearer')#, auth=AuthBearer())
def bearer(request):

    logger.warning(request)
    logger.warning(request.auth)
    return {'token': request.auth}