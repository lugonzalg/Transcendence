from ninja.errors import HttpError
from django.core.validators import validate_email
from pydantic import validator
from ninja import Schema, Field, UploadedFile, File

###############
# JWT Achemas #
###############

class JWTInput(Schema):
    username: str = Field(max_length=32, examples=["lugonzal"])
    user_id: int = Field()
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

#################
#  User Profile #
#################

class UserProfile(Schema):

    username: str
    email: str
    bio: str

username_regex = '^[A-Za-z0-9_]+$'
bio_regex = '^[a-zA-Z.,:]+$'

class User(Schema):
    
    username: str = Field(max_length=32, pattern=username_regex, examples=["walter"])
    email: str = Field(max_length=256, examples=["walter@gmail.com"])
    
    @validator('email')
    def validate_email(cls, v):

        try:
            validate_email(v)
        except Exception as err:
            raise HttpError(status_code=422, message="Bad email format")
        return v

class UserLogin(User):

    password: str = Field(min_length=12, max_length=32, examples=["This_is_my_password1!"])

    @validator('password')
    def validate_password(cls, v, values):

        if not re.search(r'[0-9]', v):
            raise HttpError(status_code=422, message="Password must contain at least one number")
        if not re.search(r'[A-Za-z]', v):
            raise HttpError(status_code=422, message="Password must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise HttpError(status_code=422, message="Password must contain at least one symbol")
        if values['username'] in v:
            raise HttpError(status_code=422, message="Password cannot contain the username")

        return v

class UserProfile(User):

    bio: str = Field(min_length=12, max_length=500, pattern=bio_regex, examples=["Lorem ipsum ... "])