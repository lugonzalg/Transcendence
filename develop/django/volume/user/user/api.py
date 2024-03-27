#CORE
from ninja import Router
from ninja.errors import HttpError

from transcendence.settings import logger
from . import crud, schemas

router = Router()

def get_user(username: str):

    db_user = crud.get_user_by_name(username)
    if not db_user:
        raise HttpError(message="Error: User Not Found", status_code=409)
    return db_user


@router.post('/add/friend')
def add_friend(request, user_id: int, friendname: str):

    db_friend = get_user(friendname)
    if not crud.add_friend(user_id, db_friend):
        raise HttpError(message="Error: Add User Failed", status_code=409)

    return {"msg": 1}

@router.delete('/delete/friend')
def delete_friend(request, user_id: int, friendname: str):

    db_friend = get_user(friendname)
    if not crud.delete_friend(user_id, db_friend.id):
        raise HttpError(message="Error: Delete User Failed", status_code=409)

    return {'msg': 1}

@router.delete('/delete/lukas')
def delete_friend(request):

    db_user = get_user('lukas')

    logger.warning(db_user)
    logger.warning(db_user.delete())

    return

@router.patch('/profile')
def update_profile(request, user_id: int, user_profile: schemas.UserProfile):

    logger.warning(f"user id: {user_id}")
    logger.warning(f"user_profile: {user_profile}")

    try:
        db_user = crud.get_user_by_id(user_id)
        logger.warning(db_user)
        db_user.username = user_profile.username
        db_user.email = user_profile.email
        db_user.save()
    except Exception as err:
        logger.error(err)
        raise HttpError(status_code=409, message="User not found")

    return {'message': 'success'}

@router.get('/profile', response=schemas.ReturnUserProfile)
def get_profile(request, user_id: int):

    db_user = crud.get_user_by_id(user_id)
    return db_user