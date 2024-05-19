import numpy as np
import queue
import threading
import asyncio
import math
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from transcendence.settings import logger

X, Y, Z = 0, 1, 2
PAD_WIDTH = 4
FIELD_WIDTH = 20
FIELD_HEIGHT = 15


class GameManager(threading.Thread):

    def __init__ (self):
        logger.warning("create game manager")
        super().__init__()
        self.tasks = {}
        self.queues = {}
        self.count = 1
        self.loop = asyncio.new_event_loop()

    def run(self):

        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def create_game(self, player_1: str, player_2: str):

        coro = self.__game(player_1, player_2)

        coro_id = f"id_{self.count}"
        self.count += 1

        self.queues[player_1] = queue.Queue()
        self.queues[player_2] = queue.Queue()

        asyncio.run_coroutine_threadsafe(coro, self.loop)
        self.tasks[coro_id] = coro
        logger.warning(f"New coro: {coro_id} added")

    def start_game(self, player: str):
        logger.warning(f"Player {player} start")
        self.queues[player].put(True)

    def echo(self):
        logger.warning("echo")

    async def __send_message(self, group_name: int, channel_type: str, message: dict):

        channel_layer = get_channel_layer()

        try:
            await channel_layer.group_send(
                group_name,
                {
                    'type': channel_type, #'add_user',  # This must match the handler function name in the consumer
                    'message': message
                }
            )
        except Exception as err:
            logger.error(err)


    async def __wait_for_players(self, player_1: str, player_2: str) -> bool:

        logger.warning(f"waiting game aproval from: {player_1} and {player_2}")
        while True:

            try:

                if not self.queues[player_1].empty() and not self.queues[player_2].empty():
                    self.queues[player_1].get()
                    self.queues[player_2].get()
                    break

                await asyncio.sleep(1)
            except Exception as err:
                logger.error(err)

        return True

    async def __handle_collisions(
        self,
        player_1,
        player_2,
        player_pads,
        ball_pos,
        ball_velocity,
        scores):

        # Check collision with player 1's paddle
        if (ball_pos[X] - 0.5 < player_pads[player_1][X] + 0.5 and
            ball_pos[X] + 0.5 > player_pads[player_1][X] - 0.5 and
            ball_pos[Z] + 0.5 > player_pads[player_1][Z] - PAD_WIDTH / 2 and
            ball_pos[Z] - 0.5 < player_pads[player_1][Z] + PAD_WIDTH / 2):

            # Calculate bounce angle
            relative_intersect_z = (ball_pos[Z] - player_pads[player_1][Z])
            normalized_intersect = relative_intersect_z / (PAD_WIDTH / 2)
            bounce_angle = normalized_intersect * (math.pi / 4)  # Adjust angle range as needed
            ball_velocity[X] = math.cos(bounce_angle)
            ball_velocity[Z] = math.sin(bounce_angle)

        # Check collision with player 2's paddle
        if (ball_pos[X] - 0.5 < player_pads[player_2][X] + 0.5 and
            ball_pos[X] + 0.5 > player_pads[player_2][X] - 0.5 and
            ball_pos[Z] + 0.5 > player_pads[player_2][Z] - PAD_WIDTH / 2 and
            ball_pos[Z] - 0.5 < player_pads[player_2][Z] + PAD_WIDTH / 2):
            # Calculate bounce angle
            relative_intersect_z = (ball_pos[Z] - player_pads[player_2][Z])
            normalized_intersect = relative_intersect_z / (PAD_WIDTH / 2)
            bounce_angle = normalized_intersect * (math.pi / 4)  # Adjust angle range as needed
            ball_velocity[X] = -math.cos(bounce_angle)
            ball_velocity[Z] = math.sin(bounce_angle)

        # Check for collisions with the top and bottom boundaries
        if ball_pos[Z] - 0.5 < -FIELD_HEIGHT / 2 or ball_pos[Z] + 0.5 > FIELD_HEIGHT / 2:
            ball_velocity[Z] = -ball_velocity[Z]

        # Check for scoring (ball passes left or right boundary)
        if ball_pos[X] - 0.5 < -FIELD_WIDTH / 2:
            scores[player_2] += 1
            # Reset ball position and velocity for a new serve
            ball_pos[:] = np.array([0, 0.5, 0], dtype=np.float32)
            ball_velocity[:] = np.array([-0.05, 0, 0], dtype=np.float32)

        elif ball_pos[X] + 0.5 > FIELD_WIDTH / 2:
            scores[player_1] += 1
            # Reset ball position and velocity for a new serve
            ball_pos[:] = np.array([0, 0.5, 0], dtype=np.float32)
            ball_velocity[:] = np.array([0.05, 0, 0], dtype=np.float32)

    async def __update_game_state(
        self,
        player_1,
        player_2,
        player_pads,
        ball_pos,
        ball_velocity,
        scores,
        group_name) -> bool:

        try:
            if not self.queues[player_1].empty():
                direction = self.queues[player_1].get()
                player_pads[player_1][Z] += (0.1 if direction else -0.1)

            if not self.queues[player_2].empty():
                direction = self.queues[player_2].get()
                player_pads[player_2][Z] += (0.1 if direction else -0.1)

            ball_pos += ball_velocity

            await self.__handle_collisions(player_1, player_2, player_pads, ball_pos, ball_velocity, scores)

            # Send updated state
            await self.__send_message(group_name, "match", {
                "ball_pos": ball_pos.tolist(),
                "player_pads": {k: v.tolist() for k, v in player_pads.items()},
                "scores": scores
            })
        except Exception as err:
            logger.error(err)

    async def __game(self, player_1: str, player_2: str):

        try:
            await self.__wait_for_players(player_1, player_2)

            group_name = f"match{player_1}_{player_2}"
            await self.__send_message(group_name, 'start', {'message':"start"})

            ball_pos = np.array([0, 0.5, 0], dtype=np.float32)
            ball_velocity = np.array([0.05, 0, 0], dtype=np.float32)
            player_pads = {
                player_1: np.array([-6.5, 0.51, 0], dtype=np.float32),
                player_2: np.array([8, 0.51, 0], dtype=np.float32)
            }
            scores = {player_1: 0, player_2: 0}
        except Exception as err:
            logger.error(err)

        logger.warning("start game")
        while True:
            try:
                await self.__update_game_state(player_1, player_2, player_pads, ball_pos, ball_velocity, scores, group_name)
                await asyncio.sleep(0.004)
                #await asyncio.sleep(1)
            except Exception as err:
                logger.error(err)