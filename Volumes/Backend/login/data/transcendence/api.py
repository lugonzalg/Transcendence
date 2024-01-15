from ninja import NinjaAPI
from login.api import router as login_router

import logging

logger = logging.getLogger("auth")

api = NinjaAPI()

api.add_router("/login/", login_router)