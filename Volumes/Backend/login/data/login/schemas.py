from ninja import Schema, ModelSchema
from pydantic import validator, Field
from . import models
from ninja.errors import HttpError
from django.core.validators import validate_email
import re

login_regex='^[A-Za-z0-9_]+$'

class UserLogin(Schema):

    username: str = Field(max_length=32, pattern=login_regex, examples=["walter"])
    password: str = Field(min_length=12, max_length=32, examples=["This_is_my_password1"])

    @validator('password')
    def validate_password(cls, v, values):

        login = values.get('username')

        if login is None:
            raise HttpError(status_code=400, message="Missing login")
        if not re.search(r'[0-9]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one number")
        if not re.search(r'[A-Z]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one symbol")
        if values['username'] in v:
            raise HttpError(status_code=404, message="Password: cannot contain the login")

        return v

class UserCreateSchema(UserLogin):

    email: str = Field(max_length=256, examples=["walter@gmail.com"])

    @validator('email')
    def validate_email(cls, v):

        try:
            validate_email(v)
        except Exception as err:
            raise HttpError(status_code=404, message="Email: bad format")
        return v
            


class UserReturnSchema(ModelSchema):

    class Meta:

        model = models.User
        fields = ['username', 'email']

class TokenReturnSchema(Schema):

    access_token: str = Field(examples=["eydlnfasdlfaks"])
    token_type: str = Field(examples=["test"])