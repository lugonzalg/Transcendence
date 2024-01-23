from ninja import Schema, ModelSchema
from pydantic import validator, Field
from . import models
from ninja.errors import HttpError
from django.core.validators import validate_email
import re

username_regex='^[A-Za-z0-9_]+$'

class Username(Schema):
<<<<<<< HEAD
    username: str = Field(max_length=32, pattern=username_regex, examples=["walter"])

class UserLogin(Username):

    password: str = Field(min_length=12, max_length=32, examples=["This_is_my_password1"])
=======
    
    username: str = Field(max_length=32, pattern=username_regex, examples=["walter"])
    
    @validator('username')
    def validate_username_length(cls, v):
        if len(v) > 16:
            raise HttpError(status_code=400, message="Username is too long")
        return v

class UserLogin(Username):

    password: str = Field(min_length=12, max_length=32, examples=["This_is_my_password1!"])
>>>>>>> origin/fix-database-migration

    @validator('password')
    def validate_password(cls, v, values):

        username = values.get('username')

        if username is None:
            raise HttpError(status_code=400, message="Missing username")
        if not re.search(r'[0-9]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one number")
        if not re.search(r'[A-Za-z]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise HttpError(status_code=404, message="Password: must contain at least one symbol")
        if values['username'] in v:
            raise HttpError(status_code=404, message="Password: cannot contain the username")

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

        model = models.user_login
        fields = ['username', 'email']

class LoginLogSchema(Schema):
    browserName: str
    browserVersion: str
    language: str
    platform: str
    screenResolution: str
<<<<<<< HEAD
    userAgent: str
=======
    userAgent: str
>>>>>>> origin/fix-database-migration
