import json
from channels.generic.websocket import WebsocketConsumer
import base64
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

        img = base64_file(message, name='yolo_picture')             #base64로 이미지 decode하기

        #모델에 적용
        model = torch.hub.load('yolov5', 'custom', path='yolo/static/21_08_30_best.pt',source='local',force_reload=True)
        results = model(img)

        results_array = results.pandas().xyxy[0].to_json(orient="records")      #결과값 json변환

       # print(type(results_array))  -> results_array : String타입
        print(results_array)

        results_array = results_array.replace("'","\"")     #'을 "로 치환해야 json으로 변환 가능함
        results_array = json.loads(results_array)       #string을 json(dict)형식으로 변환


        class_array = []
        for result in results_array:
            get_confidence = result['confidence']
            get_class = result['name']

            if get_confidence >= 0.65 :
                class_array.append(get_class)


        print(json.dumps({
                'class': class_array
            }))

        #client로 데이터 보내기기
        self.send(
            text_data=json.dumps({
                'class': class_array
            })
        )













"""
        파일io 오버헤드때문에 굳이 저장하지 x
        if default_storage.exists("test"+'/'+file.name):
            default_storage.delete("test"+'/'+file.name)

        default_storage.save("test"+'/'+file.name, file)
        print("save success")
   """
