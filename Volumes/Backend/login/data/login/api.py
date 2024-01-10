from typing import Any, Optional
from django.http import HttpRequest
from ninja.errors import HttpError

from ninja import Router
from . import schemas, crud
from transcendence import auth
import logging

logger = logging.getLogger(__name__)

router = Router()

@router.post('/create_user', response=schemas.UserReturnSchema)
def create_user(request, user: schemas.UserCreateSchema):

    logger.warning(user)
    hashed_password = auth.get_password_hash(user.password)

    return crud.create_user(user, hashed_password)



@router.get('/get_user', auth=auth.Authentication())
def get_user(request, username: str):
    db_user = crud.get_user(username)
    if db_user is None:
        raise HttpError(status_code=404, message="Error: user does not exists")