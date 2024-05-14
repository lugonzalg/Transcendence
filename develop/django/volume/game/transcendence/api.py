from ninja import NinjaAPI
from game.api import router as game


api = NinjaAPI()

api.add_router("/game/", game)