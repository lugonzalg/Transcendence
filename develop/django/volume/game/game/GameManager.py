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

    def create_game(self, p1_id: str, p2_id: str):

        coro = self.__game(p1_id, p2_id)

        coro_id = f"id_{self.count}"
        self.count += 1

        logger.warning(f"Queue created for: {p1_id}")
        self.queues[p1_id] = queue.Queue()
        logger.warning(f"Queue created for: {p2_id}")
        self.queues[p2_id] = queue.Queue()
        logger.warning(f"Current Queues: {self.queues}")

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
        player_pads,
        ball_pos,
        ball_velocity,
        scores):

        # Check collision with player 1's paddle
        if (ball_pos[X] - 0.5 < player_pads['p1'][X] + 0.5 and
            ball_pos[X] + 0.5 > player_pads['p1'][X] - 0.5 and
            ball_pos[Z] + 0.5 > player_pads['p1'][Z] - PAD_WIDTH / 2 and
            ball_pos[Z] - 0.5 < player_pads['p1'][Z] + PAD_WIDTH / 2):

            # Calculate bounce angle
            relative_intersect_z = (ball_pos[Z] - player_pads['p1'][Z])
            normalized_intersect = relative_intersect_z / (PAD_WIDTH / 2)
            bounce_angle = normalized_intersect * (math.pi / 4)  # Adjust angle range as needed
            ball_velocity[X] = math.cos(bounce_angle)
            ball_velocity[Z] = math.sin(bounce_angle)

        # Check collision with player 2's paddle
        if (ball_pos[X] - 0.5 < player_pads['p2'][X] + 0.5 and
            ball_pos[X] + 0.5 > player_pads['p2'][X] - 0.5 and
            ball_pos[Z] + 0.5 > player_pads['p2'][Z] - PAD_WIDTH / 2 and
            ball_pos[Z] - 0.5 < player_pads['p2'][Z] + PAD_WIDTH / 2):
            # Calculate bounce angle
            relative_intersect_z = (ball_pos[Z] - player_pads['p2'][Z])
            normalized_intersect = relative_intersect_z / (PAD_WIDTH / 2)
            bounce_angle = normalized_intersect * (math.pi / 4)  # Adjust angle range as needed
            ball_velocity[X] = -math.cos(bounce_angle)
            ball_velocity[Z] = math.sin(bounce_angle)

        # Check for collisions with the top and bottom boundaries
        if ball_pos[Z] - 0.5 < -FIELD_HEIGHT / 2 or ball_pos[Z] + 0.5 > FIELD_HEIGHT / 2:
            ball_velocity[Z] = -ball_velocity[Z]

        # Check for scoring (ball passes left or right boundary)
        if ball_pos[X] - 0.5 < -FIELD_WIDTH / 2:
            scores['p2'] += 1
            # Reset ball position and velocity for a new serve
            ball_pos[:] = np.array([0, 0.5, 0], dtype=np.float32)
            ball_velocity[:] = np.array([-0.05, 0, 0], dtype=np.float32)

        elif ball_pos[X] + 0.5 > FIELD_WIDTH / 2:
            scores['p1'] += 1
            # Reset ball position and velocity for a new serve
            ball_pos[:] = np.array([0, 0.5, 0], dtype=np.float32)
            ball_velocity[:] = np.array([0.05, 0, 0], dtype=np.float32)

    async def __pads_movement(
            self, 
            p1_id: str, 
            p2_id: str, 
            player_pads,
            ball_pos,
            ball_velocity,
            score,
            group_name):
        try:
            if not self.queues[p1_id].empty():
                direction = self.queues[p1_id].get()
                player_pads['p1'][Z] += (0.1 if direction else -0.1)
                await self.__update_game_state(p1_id, p2_id, player_pads, ball_pos, ball_velocity, score, group_name)

            if not self.queues[p2_id].empty():
                direction = self.queues[p2_id].get()
                player_pads['p2'][Z] += (0.1 if direction else -0.1)
                await self.__update_game_state(p1_id, p2_id, player_pads, ball_pos, ball_velocity, score, group_name)

        except Exception as err:
            logger.warning(err)

    async def __update_game_state(
        self,
        p1_id,
        p2_id,
        player_pads,
        ball_pos,
        ball_velocity,
        scores,
        group_name) -> bool:

        try:

            ball_pos += ball_velocity

            await self.__handle_collisions(player_pads, ball_pos, ball_velocity, scores)

            # Send updated state
            await self.__send_message(group_name, "match", {
                "ball_pos": ball_pos.tolist(),
                "player_pads": {k: v.tolist() for k, v in player_pads.items()},
                "scores": scores
            })
        except Exception as err:
            logger.error(err)

    async def __game(self, p1_id: str, p2_id: str):

        try:
            await self.__wait_for_players(p1_id, p2_id)

            group_name = f"match{p1_id}_{p2_id}"
            await self.__send_message(group_name, 'start', {'message':"start"})

            ball_pos = np.array([0, 0.5, 0], dtype=np.float32)
            ball_velocity = np.array([0.05, 0, 0], dtype=np.float32)
            player_pads = {
                'p1': np.array([-6.5, 0.51, 0], dtype=np.float32),
                'p2': np.array([8, 0.51, 0], dtype=np.float32)
            }
            scores = {'p1': 0, 'p2': 0}
        except Exception as err:
            logger.error(err)

        logger.warning("start game")
        frame = 16
        while True:
            try:

                if frame == 0:
                    await self.__update_game_state(p1_id, p2_id, player_pads, ball_pos, ball_velocity, scores, group_name)
                    frame = 16

                await self.__pads_movement(p1_id, p2_id, player_pads, ball_pos, ball_velocity, scores, group_name)

                frame -= 1
                await asyncio.sleep(0.002)
            except Exception as err:
                logger.error(err)