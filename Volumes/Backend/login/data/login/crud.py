from ninja.errors import HttpError
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from . import schemas, models

def create_user(user: schemas.UserCreateSchema, hashed_password: str):
    user = user.model_dump()
    try:
        db_user = models.User.objects.create(
            login=user['login'],
            password=hashed_password,
            email=user['email'])

    except IntegrityError as err:
        raise HttpError(status_code=400, message="Error: user already exists")

    return db_user

def get_user(login: str):

    try:
        db_user = models.User.objects.filter(login=login).get()
    except IntegrityError:
        raise HttpError(status_code=400, message="Error: user already exists")
    except ObjectDoesNotExist:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    return db_user