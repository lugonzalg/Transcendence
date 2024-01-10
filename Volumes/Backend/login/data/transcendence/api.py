from ninja.errors import HttpError
from ninja import NinjaAPI, Form
from login.api import router as login_router

from login import params, schemas
from . import auth

import logging

logger = logging.getLogger("auth")

api = NinjaAPI()

api.add_router("/login/", login_router)

@api.post('/token', response=schemas.TokenReturnSchema)
def login(request, user: schemas.UserLogin) -> schemas.TokenReturnSchema:

    if auth.authenticate_user(user.username, user.password):
        raise HttpError(status_code=403, message="Error: Unauthorized")

    access_token = auth.get_jwt(user.username, params.COMMON_USER)
    token = schemas.TokenReturnSchema(token=access_token, token_type="test")
    
    return token
