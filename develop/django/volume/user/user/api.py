#CORE
from ninja import Router, File, UploadedFile
from ninja.errors import HttpError

from transcendence.settings import logger
from . import crud, schemas

from user.consumers import ws_users

from typing import Optional
import requests

router = Router()

def get_user(username: str):

    try:
        db_user = crud.get_user_by_name(username)
        return db_user
    except Exception as err:
        logger.error(err)

    return None

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_message_to_channel(user_id: int, channel_type: str, message: dict):

    channel_layer = get_channel_layer()

    logger.warning(f'message: {message}')
    # Send message to user-specific group
    retval = async_to_sync(channel_layer.group_send)(
        f'user_{user_id}',  # Group name must match the one used in the consumer
        {
            'type': channel_type, #'add_user',  # This must match the handler function name in the consumer
            'message': message
        }
    )

@router.post('/add', response=schemas.ReturnUserData)
def add_friend(request, user_id: int, username: str, friendname: str):

    db_friend = get_user(friendname)
    if db_friend is None:
        raise HttpError(status_code=400, message="User does not exist")

    logger.warning(f"user exists: {db_friend.username}")
    if not crud.add_friend(user_id, db_friend):
        raise HttpError(status_code=409, message="Add User Failed")

    message = {'id': user_id, 'username': username, 'online': True, 'challenge': 0}
    send_message_to_channel(db_friend.id, 'add_user', message)

    return db_friend

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

@router.post('/profile')
def update_profile(request,
                   user_id: int,
                   image: File[UploadedFile],
                   username: str | None = None,
                   email: str | None = None,
                   bio: str | None = None):

    logger.warning(f"user id: {user_id}")

    try:
        db_user = crud.get_user_by_id(user_id)
    except Exception as err:
        logger.error(err)
        raise HttpError(status_code=409, message="User not found")

    if username:
        db_user.username = username

    if db_user.mode == 0 and email:
        db_user.email = email

    if image:
        logger.warning(f"New image for user: {db_user.username}")
        with open(f"/avatar/{user_id}.png", 'wb') as fd:
            fd.write(image.file.read())
        db_user.avatar = f"/avatar/{user_id}.png"

    db_user.save()

    return {'message': 'success'}

@router.get('/profile', response=schemas.ReturnUserProfile)
def get_profile(request, user_id: int):

    db_user = crud.get_user_by_id(user_id)
    return db_user

import datetime

def check_status(last_log):
    logger.warning(f"Check status: {type(last_log)}")
    now = datetime.datetime.now()

    logger.warning('Check status')
    logger.warning(now - last_log.replace(tzinfo=None))
    logger.warning(datetime.timedelta(minutes=30))

    if now - last_log.replace(tzinfo=None) < datetime.timedelta(minutes=1440):
        return True
    return False

from typing import List

@router.get('/friend/list')
def get_friend_list(request, user_id: int):

    friend_list = crud.get_friend_list(user_id)
    if friend_list is None:
        raise HttpError(status_code=409, message='Fetching friend list failed')

    friends = [{'username': friend[0].username,
               "lastActive": friend[0].last_log,
               "id": friend[0].id,
               "status": friend[1],
               "challenge": friend[2],
               "online": check_status(friend[0].last_log) } for friend in friend_list]

    logger.warning(friends)
    return friends

@router.post('/friend/request')
def friend_request(request, status: bool, user_id: int, friend_id: int):

    #Accept request
    if status == 1:
        if not crud.accept_friend_request(user_id, friend_id):
            raise HttpError(status_code=409, message='Accept friend request failed')

        message = {'id': user_id, 'online': True, 'challenge': 0}
        send_message_to_channel(friend_id, 'accept_user', message)
        return {'message': 'Friend accept request succed'}

    #decline request
    if not crud.decline_friend_request(user_id, friend_id):
        raise HttpError(status_code=409, message='Decline friend request failed')

    message = {'id': user_id}
    send_message_to_channel(friend_id, 'decline_user', message)
    return {'message': 'Friend decline request succed'}

@router.post('/challenge')
def request_challenge(request, user_id: int, friend_id: int):

    if not crud.create_challenge(user_id, friend_id):
        raise HttpError(status_code=409, message='Challenge failed')

    message = {'id': user_id}
    send_message_to_channel(friend_id, 'challenge_user', message)
    return {'message': 'challenge success'}

@router.post('/challenge/response')
def challenge_response(request, user_id: int, friend_id: int, response: int):

    if response:
        if not crud.accept_challenge(user_id, friend_id):
            raise HttpError(status_code=409, message='Challenge accept failed')

        message = {'id': user_id}
        send_message_to_channel(friend_id, 'accept_challenge', message)

        if not create_match(user_id, friend_id):
            raise HttpError(status_code=404, message='match creation failed')
        return {'message': 'Challenge accepted'}

    if not crud.deny_challenge(user_id, friend_id):
        raise HttpError(status_code=409, message='Challenge deny failed')

    message = {'id': user_id}
    send_message_to_channel(friend_id, 'deny_challenge', message)
    return {'message': 'Challenge denied'}

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Function to add users dynamically to a shared channel
def create_match(user_1: int, user_2: int) -> bool:
    channel_layer = get_channel_layer()
    group_name = f'match{user_1}_{user_2}'
    
    logger.warning(ws_users)
    logger.warning(f"p1: {user_1}")
    logger.warning(f"p2: {user_2}")
    # Loop through each user to add their channel to the group

    user_1 = ws_users.get(user_1)
    user_2 = ws_users.get(user_2)

    match_data = {
        "1" : {
                "username" : user_1.user.username,
                "avatar": user_1.user.avatar
            },
        "2":
            {
                "username" : user_2.user.username,
                "avatar": user_2.user.avatar
            }
    }
    for idx, user in enumerate([user_1, user_2]):
        logger.warning(f"test: {user.channel_name}")
        
        # Perform group add synchronously
        async_to_sync(channel_layer.group_add)(
            group_name,  # New shared group name
            user.channel_name  # User-specific channel name
        )


        user_room = f'user_{user.user.id}'
        async_to_sync(channel_layer.group_send)(
            user_room,
            {
                "type": "match",
                "message": match_data
            }
        )

    params = {
        'p1_id': user_1.user.id,
        'p2_id': user_2.user.id
    }

    res = safe_post('create_match', 'http://game:7777/api/game/create', params=params)

    logger.warning('create subprocess')
    if res is None or not res.ok:
        logger.error('game creation failed')
        return False

    logger.warning('succed')
    return True

def safe_post(context: str, url: str, params: dict = None, json: dict = None) -> Optional[object]:

    try:
        res = requests.post(url, params=params, json=json)

        return res
    except Exception as err:
        logger.error(f'Exception for {context}: {err}')

    return None