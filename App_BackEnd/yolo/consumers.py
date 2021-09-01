import asyncio
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class sendConsumer(WebsocketConsumer):
    def connect(self):
        print("connected")
        self.accept()


    def disconnect(self, code):
        print("disconnected")


    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
