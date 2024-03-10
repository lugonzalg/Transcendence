from ninja.errors import HttpError
from django.core.validators import validate_email
from ninja import Schema, Field
from pydantic import validator

###############
# JWT Achemas #
###############

class JWTInput(Schema):
    username: str = Field(max_length=32, examples=["lugonzal"])
    expire_time: int = Field(ge=5, default=30)
    permission: int = Field(default=1)

class JWTToken(Schema):

    token: str
    refresh: str

class UserLogin(Schema):

    username: str
    password: str

class UserRegister(UserLogin):

    email: str