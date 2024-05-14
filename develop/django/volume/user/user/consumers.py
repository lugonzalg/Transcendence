# chat/consumers.py
from enum import Enum

import json

from transcendence.settings import logger
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


TEST = 0
ADD_USER = 1
ACCEPT_USER = 2
DECLINE_USER = 3
CHALLENGE_USER = 4
ACCEPT_CHALLENGE = 5
DENY_CHALLENGE = 6
TOURNAMENT = 7
MATCH = 8

ws_users = {}

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = "user_%s" % self.user.id
        self.channels = []

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        ws_users[self.user.id] = self

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        for channel in self.channels:
            async_to_sync(self.channel_layer.group_discard)(
                channel,
                self.channel_name
            )

    def add_channel(self, channel: str):
        self.channels.append(channel)

    # Receive message from WebSocket
    def receive(self, text_data):

        logger.warning("Message received from user")
        logger.warning(text_data)

        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat_message", "message": message}
            )
        except Exception as err:
            logger.error(err)


    def _send_event(self, event_type: int, message: dict):

        # Send message to WebSocket
        self.send(text_data=json.dumps({"type": event_type, "message": message}))

    def add_user(self, event):
        logger.warning("add user")
        message = event["message"]

        self._send_event(ADD_USER, message)

    # Receive message from room group
    def accept_user(self, event):
        logger.warning("accept user")
        message = event["message"]

        self._send_event(ACCEPT_USER, message)

    def decline_user(self, event):
        logger.warning("decline user")
        message = event["message"]

        self._send_event(DECLINE_USER, message)

    def challenge_user(self, event):
        logger.warning("challenge user")
        message = event["message"]

        self._send_event(CHALLENGE_USER, message)

    def accept_challenge(self, event):
        logger.warning("accept challenge")
        message = event["message"]

        self._send_event(ACCEPT_CHALLENGE, message)

    def deny_challenge(self, event):
        logger.warning("deny challenge")
        message = event["message"]

        self._send_event(DENY_CHALLENGE, message)

    def tournament(self, event):
        logger.warning("tournament")
        message = event["message"]

        self._send_event(TOURNAMENT, message)


    def match(self, event):
        logger.warning("match")
        message = event["message"]

        self._send_event(MATCH, message)

    def test(self, event):
        logger.warning("match")
        message = event["message"]

        self._send_event(TEST, message)