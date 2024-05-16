from transcendence.settings import logger
from multiprocessing import Process
import asyncio
import time
import numpy as np

from ninja import Router
from ninja.errors import HttpError

router = Router()

referee = {}

@router.get('/ok')
def game_service_ok(request):
    return {"message": "ok"}

def game(p1: str, p2: str):

    message = {"message": "start"}
    group_name = f"match{p1}_{p2}"

    send_message_to_channel(group_name, 'start', message)
    ball_position = np.array([0, 0.5, 0], dtype=np.float32)
    ball_velocity = np.array([0.05, 0, 0.00], dtype=np.float32)
    p1_paddle_position = np.array([-6.5, 0.51, 0], dtype=np.float32)
    p2_paddle_position = np.array([8, 0.51, 0], dtype=np.float32)
    p1_score = 0
    p2_score = 0

    while True:

        # Efficiently update positions using NumPy
        ball_position += ball_velocity

        # Example: Reverse velocity if a boundary is hit
        if ball_position[2] <= -5.4 or ball_position[2] >= 5.4:
            ball_velocity[2] = -ball_velocity[2]

        # Convert NumPy arrays to lists for JSON serialization
        state = {
            "ball_position": ball_position.tolist(),
            "p1_paddle_position": p1_paddle_position.tolist(),
            "p2_paddle_position": p2_paddle_position.tolist(),
            "scores": [p1_score, p2_score]
        }
        send_message_to_channel(group_name, 'match', state)

        time.sleep(0.032)  # Approx 60fps

@router.post('/create')
async def create_game(request, p1_id: str, p2_id: str):

    game_process = Process(target=game, args=(p1_id, p2_id))

    referee[p1_id] = 0
    referee[p2_id] = 0

    while True:

        if referee.get(p1_id) and referee.get(p2_id):
            logger.warning('start game!')
            break

        await asyncio.sleep(1)

    del referee[p1_id]
    del referee[p2_id]

    game_process.start()

    return {'message': 'game created'}

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_message_to_channel(group_name: int, channel_type: str, message: dict):

    channel_layer = get_channel_layer()

    #logger.warning(f'message: {message}')
    # Send message to user-specific group
    retval = async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': channel_type, #'add_user',  # This must match the handler function name in the consumer
            'message': message
        }
    )

@router.get('/start')
def game_start(request, user_id: str):

    logger.warning(f"user_id: {user_id}")
    logger.warning(referee)

    if user_id not in referee:
        raise HttpError(status_code=400, message=f'unable to set referee for {user_id}')

    referee[user_id] = 1
    return {'message': 'start'}