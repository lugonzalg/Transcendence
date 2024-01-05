from ninja import NinjaAPI
from login.api import router as login_router

api = NinjaAPI()

api.add_router("/login/", login_router)