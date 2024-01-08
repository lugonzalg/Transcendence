from passlib.context import CryptContext
from ninja.security import HttpBearer

from datetime import datetime, timedelta
import os
from jose import JWTError, jwt

from login import schemas, crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def create_access_token(
        data: dict, 
        expires_delta: timedelta | None = None,
        ) -> str:

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ['SECRET_KEY'], algorithm=os.environ['ALGORITHM'])
    return encoded_jwt

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(login: str, password: str):
    user = crud.get_user(login)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

import logging

logger = logging.getLogger(__name__)

class Authentication(HttpBearer):

    def authenticate(self, request, token):
        decoded = jwt.decode(token, os.environ['SECRET_KEY'], os.environ['ALGORITHM'])
        logger.warning(decoded)
        if token == "supersecret":
            return token

def get_jwt(login: str, level: int) -> str:

    access_token_expires = timedelta(minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]))

    access_token = create_access_token(
        data={'sub': login, 'level': level}, expires_delta=access_token_expires
    )
    return access_token
