from transcendence.settings import logger
import asyncio
import time
from game.GameManager import GameManager

from ninja import Router
from ninja.errors import HttpError

router = Router()

game_manager = None

@router.get('/ok')
def game_service_ok(request):
    return {"message": "ok"}

@router.get('/echo')
def echo_game_manager(request):
    #global game_manager

    #game_manager.echo()
    global game_manager

    #game_process = Process(target=game, args=(p1_id, p2_id))
    if game_manager is None:
        logger.warning("Game manager not found, creating one!")
        game_manager = GameManager()
        game_manager.start()

    game_manager.create_game("1", "2")

    return {"message": "ok"}

@router.post('/create')
def create_game(request, p1_id: str, p2_id: str):

    global game_manager

    if game_manager is None:
        game_manager = GameManager()
        game_manager.start()

    game_manager.create_game(p1_id, p2_id)
    return {'message': 'game created'}

@router.get('/start')
def game_start(request, user_id: str):

    logger.warning(f"user_id: {user_id}")

    if game_manager is None or user_id not in game_manager.queues:
        raise HttpError(status_code=400, message=f'unable to set referee for {user_id}')

    game_manager.start_game(user_id)

    return {'message': 'start'}

@router.get('/move')
def move_pad(request, user_id: str, direction: bool):

    if user_id in game_manager.queues:
        game_manager.queues[user_id].put(direction)

    return {'message': 'moved'}