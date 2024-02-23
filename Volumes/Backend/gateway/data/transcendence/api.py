from ninja import NinjaAPI
from gateway.api import router as gateway_router

api = NinjaAPI()

api.add_router("/", gateway_router)