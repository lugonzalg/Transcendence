from ninja import Schema, ModelSchema
from pydantic import validator, Field
from . import models
from ninja.errors import HttpError
import re

login_regex='^[A-Za-z0-9_]+$'

class UserLogin(Schema):

    login: str = Field(max_length=32, pattern=login_regex, examples=["walter"])
    password: str = Field(min_length=12, max_length=32, examples=["This_is_my_password1"])

class UserCreateSchema(UserLogin):

    email: str = Field(max_length=256, examples=["walter@gmail.com"])

    @validator('password')
    def validate_password(cls, v, values):

        if not re.search(r'[0-9]', v):
            raise HttpError(status_code=404, message="Password must contain at least one number")
        if not re.search(r'[A-Z]', v):
            raise HttpError(status_code=404, message="Password must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise HttpError(status_code=404, message="Password must contain at least one symbol")
        if values['login'] in v:
            raise HttpError(status_code=404, message="Password cannot contain the login")

        return v

class UserReturnSchema(ModelSchema):

    class Meta:

        model = models.User
        fields = ['login', 'email']

class TokenReturnSchema(Schema):

    token: str