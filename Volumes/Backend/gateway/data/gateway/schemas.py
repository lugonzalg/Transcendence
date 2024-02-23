from ninja.errors import HttpError
from django.core.validators import validate_email
from ninja import Schema, Field
from pydantic import validator

###############
# JWT Achemas #
###############

class JWTInput(Schema):
    email: str = Field(max_length=256, examples=["walter@gmail.com"])

    @validator('email')
    def validate_email(cls, v):

        try:
            validate_email(v)
        except Exception as err:
            raise HttpError(status_code=404, message="Email: bad format")
        return v
    expire_time: int = Field(ge=5, default=30)
    permission: int = Field(default=1)

class JWTToken(Schema):

    token: str
    refresh: str