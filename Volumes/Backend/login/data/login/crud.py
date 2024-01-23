from ninja.errors import HttpError
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from . import schemas, models
from .models import user_login
from transcendence import Logger

logger = Logger.Logger(name="login")

<<<<<<< HEAD
def create_user(user: schemas.UserCreateSchema) -> models.User:

    try:

        db_user = models.User.objects.create(
            username=user.username,
            password=make_password(user.password),
            email=user.email)

=======

def create_user(user: schemas.UserCreateSchema) -> models.user_login:
    try:
        db_user = models.user_login.objects.create(
            username=user.username,
            password=make_password(user.password),
            email=user.email)
        logger.info(f"Usuario creado con éxito: {db_user.username}")
>>>>>>> origin/fix-database-migration
    except IntegrityError as err:
        error_msg = str(err)
        if 'username' in error_msg:
            raise HttpError(status_code=409, message="Error: Username already exists")
        elif 'email' in error_msg:
            raise HttpError(status_code=409, message="Error: Email already exists")
        else:
            raise HttpError(status_code=409, message="Error: User already exists")
    return db_user

def get_user(username: str):
    try:
        logger.warning(f"Searching for username: {username}")
        db_user = user_login.objects.filter(username=username).get()
        logger.warning(f"User found: {db_user.username}")
    except user_login.DoesNotExist:
        logger.error(f"User not found: {username}")
        raise HttpError(status_code=403, message="Error: Unauthorized")
    except MultipleObjectsReturned:
        logger.error(f"Multiple users found for: {username}")
        raise HttpError(status_code=409, message="Error: Multiple users found")
    except IntegrityError:
        logger.error(f"Integrity error for: {username}")
        raise HttpError(status_code=500, message="Integrity error")
    except Exception as e:
        logger.error(f"Unexpected error for {username}: {e}")
        raise HttpError(status_code=500, message=f"Internal Server Error: {e}")

    return db_user
