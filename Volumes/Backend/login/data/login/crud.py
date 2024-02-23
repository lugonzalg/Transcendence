from ninja.errors import HttpError
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
from . import schemas, models
from .models import user_login
from transcendence.settings import logger
from django.core.exceptions import ObjectDoesNotExist

def create_user(user: schemas.UserCreateSchema, mode: int) -> models.user_login:
    try:
        db_user = models.user_login.objects.create(
            username=user.username,
            password=make_password(user.password),
            email=user.email,
            mode=mode)
        logger.info(f"Usuario creado con éxito: {db_user.username}")
    except IntegrityError as err:
        error_msg = str(err)
        if 'username' in error_msg:
            raise HttpError(status_code=409, message="Error: Username already exists")
        elif 'email' in error_msg:
            raise HttpError(status_code=409, message="Error: Email already exists")
        else:
            raise HttpError(status_code=409, message="Error: User already exists")
        #si se ha autentificado con otro metodo error tambien 
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

def get_user_by_email(email: str) -> models.user_login | None:

    try:
        print(f"email: {email}")
        db_user = models.user_login.objects.all()
        print(len(db_user))

        db_user = models.user_login.objects.filter(email=email).get()
        return db_user

    except ObjectDoesNotExist as err:
        logger.error(f"Error: Not Found {err}")

    except Exception as err:
        logger.error(f"Error: Unhandled {err}")