from ninja.errors import HttpError
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from . import schemas, models
import logging

logger = logging.getLogger(__name__)

def create_user(user: schemas.UserCreateSchema, hashed_password: str):
    user = user.model_dump()
    try:
        logger.warning(user)
        logger.warning(user['username'])
        logger.warning(user['email'])

        db_user = models.User.objects.create(
            username=user['username'],
            password=hashed_password,
            email=user['email'])

    except IntegrityError as err:
        raise HttpError(status_code=409, message="Error: user already exists")

    return db_user

def get_user(username: str):

    try:
        db_user = models.User.objects.filter(username=username).get()
    except IntegrityError:
        raise HttpError(status_code=409, message="Error: user already exists")
    except ObjectDoesNotExist:
        raise HttpError(status_code=403, message="Error: Unauthorized")

    return db_user