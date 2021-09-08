import json
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import default_storage


def base64_file(data, name=None):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data



class sendConsumer(WebsocketConsumer):
    def connect(self):
       # print("connected")
        self.accept()


    def disconnect(self, code):
        # print("disconnected")
        pass


    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        nickname = str(data['nickname'].encode("utf-8"))

        file = base64_file(message, name='yolo_picture')
        file.name = nickname + ".png"

        if default_storage.exists("test"+'/'+file.name):
            default_storage.delete("test"+'/'+file.name)

        default_storage.save("test"+'/'+file.name, file)
        print("save success")

