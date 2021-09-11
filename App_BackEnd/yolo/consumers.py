import json
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import default_storage
import cv2
import torch
from PIL import Image
from io import BytesIO

def base64_file(data, name=None):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    return data

def copy_attr(a, b, include=(), exclude=()):
    # Copy attributes from b to a, options to only include [...] and to exclude [...]
    for k, v in b.__dict__.items():
        if (len(include) and k not in include) or k.startswith('_') or k in exclude:
            continue
        else:
            setattr(a, k, v)


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
        nickname = data['nickname']

        file = base64_file(message, name='yolo_picture')
        file.name = nickname + ".jpg"







"""
        파일io 오버헤드때문에 굳이 저장하지 x
        if default_storage.exists("test"+'/'+file.name):
            default_storage.delete("test"+'/'+file.name)

        default_storage.save("test"+'/'+file.name, file)
        print("save success")
   """
