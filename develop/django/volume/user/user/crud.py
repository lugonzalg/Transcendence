#Errores
from django.db.utils import IntegrityError
from ninja.errors import HttpError
from django.core.exceptions import MultipleObjectsReturned

from transcendence.settings import logger
from user.models import user_login, Friends

def get_user_by_id(user_id: int):
    try:
        logger.warning(f"Searching for user_id: {user_id}")
        db_user = user_login.objects.filter(id=user_id).get()
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

def get_user_by_name(username: str):
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

def add_friend(user_id: int, db_user: user_login) -> bool:

    try:
        relation_1 = Friends(
            user_id=user_id,
            friend_id=db_user.id,
            status=0
        )
        relation_1.save()

        relation_2 = Friends(
            user_id=db_user.id,
            friend_id=user_id,
            status=1
        )
        relation_2.save()
    except Exception as err:
        logger.error(err)
        return False

    return True

def delete_friend(user_id: int, friend_id: int):

    try:
        relation_1 = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
        relation_2 = Friends.objects.filter(user_id=friend_id, friend_id=user_id)

        relation_1.delete()
        relation_2.delete()

    except Exception as err:
        logger.error(err)
        return False
    return True

def get_friend_list_by_id(user_id: int):

    try:
        friend_list = Friends.objects.filter(user_id=user_id)
    except Exception as err:
        raise HttpError(status_code=409, message='Fetching friend list failed')
    return friend_list

from django.db.models import Q
from typing import List, Optional

def get_friend_list(user_id: int) -> Optional[List[user_login]]:
    try:
        # Query to find where the user is either the 'user' or the 'friend' in the Friends model
        friends_relations = Friends.objects.filter(Q(user_id=user_id))

        # Collect all user_login objects corresponding to the friends of db_user
        friends = set()
        for relation in friends_relations:
            if relation.user_id == user_id:
                friends.add((relation.friend, relation.status, relation.challenge))

        return list(friends)

    except Exception as err:
        logger.error(err)

    return None

def accept_friend_request(user_id: int, friend_id: int) -> bool:

    try:
        friends_relations = Friends.objects.filter(Q(user_id=user_id) | Q(user_id=friend_id))

        for relation in friends_relations:
            relation.status = 2
            relation.save()

        return True

    except Exception as err:
        logger.error(err)

    return False

def decline_friend_request(user_id: int, friend_id: int) -> bool:

    try:
        friends_relations = Friends.objects.filter(Q(user_id=user_id) | Q(user_id=friend_id))

        for relation in friends_relations:
            relation.delete()

        return True

    except Exception as err:
        logger.error(err)

    return False

def create_challenge(user_id: int, friend_id: int) -> bool:

    try:
        friends_relations = Friends.objects.filter(Q(user_id=user_id) & Q(friend_id=friend_id) | Q(friend_id=user_id) & Q(user_id=friend_id))

        for relation in friends_relations:
            if relation.user_id == user_id:
                relation.challenge = 2
            else:
                relation.challenge = 1
            relation.save()
        return True

    except Exception as err:
        logger.error(err)

    return False

def accept_challenge(user_id: int, friend_id: int):

    try:
        friends_relations = Friends.objects.filter(Q(user_id=user_id) & Q(friend_id=friend_id) | Q(friend_id=user_id) & Q(user_id=friend_id))

        for relation in friends_relations:
            relation.challenge = 3
            relation.save()
        return True
    except Exception as err:
        logger.error(err)

    return False

def deny_challenge(user_id: int, friend_id: int):

    try:
        friends_relations = Friends.objects.filter(Q(user_id=user_id) & Q(friend_id=friend_id) | Q(friend_id=user_id) & Q(user_id=friend_id))

        for relation in friends_relations:
            relation.challenge = 0
            relation.save()
        return True
    except Exception as err:
        logger.error(err)

    return False