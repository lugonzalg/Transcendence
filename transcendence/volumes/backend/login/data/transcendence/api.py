from ninja import NinjaAPI, Form
from login.api import router as login_router
from datetime import datetime, timedelta
import os
from jose import JWTError, jwt

import login.schemas as schemas

api = NinjaAPI()

api.add_router("/login/", login_router)

def create_access_token(data: dict, expires_delta: timedelta | None = None):

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ['SECRET_KEY'], algorithm=os.environ['ALGORITHM'])
    return encoded_jwt

#@api.post('/login', response=schemas.TokenReturnSchema)
#def login(request, user: schemas.UserLogin):
#
#    return {"token": "qwerty"}

@api.post('/login')
def login(request, username: Form[str], password: Form[str]):
    return {"username": "qwer", "password": "test"}

