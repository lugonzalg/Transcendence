from transcendence.settings import logger
from channels.db import database_sync_to_async
from user.models import user_login

import user.crud as crud

@database_sync_to_async
def get_user(user_id: int) -> user_login | None:
    try:
        return crud.get_user_by_id(user_id)
    except user_login.DoesNotExist:
        return None

import requests

class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).

        headers = scope.get('headers', None)

        auth = None
        if headers is None:
            return None

        for header in headers:
            if header[0] == b'cookie':
                cookie = header
                break

        if cookie is None or len(cookie) != 2:
            return None

        payload = {'jwt': cookie[1].decode()}
        res = requests.post('http://gateway:4242/api/auth', params=payload)

        if not res.ok:
            return None

        jwt_data = res.json()

        scope['user'] = await get_user(int(jwt_data["user_id"]))

        return await self.app(scope, receive, send)