import json
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import default_storage
import cv2
import torch
from PIL import Image
from io import BytesIO
import numpy as np

def base64_file(data, name=None):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    str_decoded = base64.b64decode(imgstr)

    jpg_as_np = np.frombuffer(str_decoded, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)

    return img


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
      #  nickname = data['nickname']

        img = base64_file(message, name='yolo_picture')

        model = torch.hub.load('../yolov5', 'custom', path='/static/21_08_30_best.pt',source='local',force_reload=True)
        results = model(img)

        print(results.pandas().xyxy[0].to_json(orient="records"))










"""
        파일io 오버헤드때문에 굳이 저장하지 x
        if default_storage.exists("test"+'/'+file.name):
            default_storage.delete("test"+'/'+file.name)

        default_storage.save("test"+'/'+file.name, file)
        print("save success")
   """
