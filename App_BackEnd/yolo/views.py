from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
import jwt
import json
import base64
import cv2
import torch
import numpy as np
from django.utils import timezone
from api.models import User
from study.models import Daily_1m_content

def base64_file(data, name=None):
    if data is None:
        return "none"
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]
    str_decoded = base64.b64decode(imgstr)

    jpg_as_np = np.frombuffer(str_decoded, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, cv2.IMREAD_COLOR)

    return img

global total_play, total_con
global array
array = []

class getmessage(views.APIView):
   # global array
   # array = []

    def post(self, request):

        global total_play, total_con, array

        #토큰 받아오기

        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])

        #이미지 base64 디코딩
      #  message = self.request.query_params.get('message')
        message= request.data.get("message")
        img = base64_file(message, name='yolo_picture')  # base64로 이미지 decode하기
        if img =="none" :
            print("no picture")
            type = 'P'
        else :

            # 모델에 적용
            model = torch.hub.load('yolov5', 'custom', path='yolo/static/best.pt', source='local', force_reload=True)
            results = model(img)

            results_array = results.pandas().xyxy[0].to_json(orient="records")  # 결과값 json변환

            results_array = results_array.replace("'", "\"")  # '을 "로 치환해야 json으로 변환 가능함
            results_array = json.loads(results_array)  # string을 json(dict)형식으로 변환



            class_array = []
            for result in results_array:
                get_confidence = result['confidence']
                get_class = result['name']

                if get_confidence >= 0.1:
                    class_array.append(get_class)

            if 'face' in class_array:
                type = 'P'
                # message = 'yes face'
            else:
                if ('book' in class_array) or ('tablet' in class_array):
                    if 'phone' in class_array:
                        type = 'P'
                    #   message = 'handphone'

                    else:
                        if 'handonly' in class_array:
                            type = 'C'
                        #   #     message = 'handonly'
                        elif 'pen' in class_array:
                            type = 'C'

                        else:
                            type = 'P'
                        #       message='none'

                else:
                    type = 'P'
                    # message = 'no face no desk'

            print("type => " + type)

        # 같은 시간 내에 최대 20개 모아서 1분으로 저장
        now = timezone.now()
        hour = now.hour
        minute = now.minute
        time = str(hour) + ":" + str(minute)


        #각각 user의 time마다 type저장해줌
      #  user_Exists=False
        if len(array) != 0:
            for a in array :
                if a[0] == user :    #이미 저장된 type이 존재하는 경우
                    time_Exists=False
                  #  user_Exists=True
                    for t in a[1] :     #a[1] = [ [time,[type]] ,  [time,[type]] , ... ]
                        if t[0] == time :       #배열 내 time 존재하는 경우
                            t[1].append(type)
                            time_Exists=True
                            print("2:")
                            print(array)

                            break
                        if not time_Exists : #같은 시간대 존재하지 않는 경우 새로 저장해 줌
                            a[1].append([time,[type]])
                            print("3")
                            print(array)
        else:
            array.append([user,[[time,[type]]]])

            print("1")
            print(array)

        index = 0
        for data in array :     #data = [user, [   [time,[type]] ,  [time,[type]] , ... ] ]

            if data[0] == user :        #user의 [user, [   [time,[type]] ,  [time,[type]] , ... ] ] 찾은 경우

                for a in data[1] :  # data[1] =[   [time,[type]] ,  [time,[type]] , ... ] 중에서 a =[time,[type]]
                    concent = 0
                    play = 0
                    if a[0] == time :
                        for t in a[1]:      # a[1]= [type, type, ... ] , t =각각 type들 원소 하나
                                        #돌면서 type 개수가 20개이면 1분 데이터로 저장 위해 개수 세기
                            if t == 'C':
                                concent += 1
                            elif t == 'P':
                                play += 1
                        if concent + play == 12 :           #12개면 1m 데이터로 저장하기
                            if concent >= play :        #C 로 저장
                                Daily_1m_content.objects.create(uid=user, type='C', time=time).save()

                            else :          #P 로 저장
                                Daily_1m_content.objects.create(uid=user, type='P', time=time).save()

                            #d_1m 만들어지면 array 비우기
                            array.remove(array[index])

                            print("20 success and delete from array => " + time + "and type is  => " + type)
            index += 1


        return Response({'type': type},status=status.HTTP_200_OK)

