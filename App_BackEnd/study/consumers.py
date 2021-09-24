import threading
from time import sleep
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
import json
from main.models import Room_Enroll
from .models import Daily_1m_content
import jwt
from api.models import User

def get_time(count):

    if count < 60:
        hour = 0
    else :
        hour = count // 60

    minute = count - hour * 60
    if minute < 10 :
        minute = "0" + str(minute)
    time = str(hour) + ":" + str(minute)
    return time



class sendMate(WebsocketConsumer):


    def connect(self):
        self.accept()



    def websocket_disconnect(self, code):
        self.stop = True
        del self.thread
        raise StopConsumer()



    def action(self, room_query, token_uid):
        while True:

            studymates = []
            for room in room_query:

                user = room.user_id
                study_info = Daily_1m_content.objects.filter(uid=user)
                concent = 0
                play = 0

                for info in study_info:  # 실시간 play/concent 개수 가져오기
                    if info.type == 'C':
                        concent += 1
                    elif info.type == 'P':
                        play += 1

                tot_time = study_info.count()
                if concent == 0:
                    concent_rate = '0'
                else:
                    concent_rate = round(concent / tot_time, 2) * 100

                concent_time = get_time(concent)
                concent_time = concent_time.split(":")[0] + "시간 " + concent_time.split(":")[1] + "분"

                play_time = get_time(play)
                play_time = play_time.split(":")[0] + "시간 " + play_time.split(":")[1] + "분"

                if user.uid != token_uid:
                    studymates.append({
                        "nickname": user.nickname,
                        "concent_rate": str(concent_rate) + "%",
                        "concent_time": concent_time,
                        "play_time": play_time
                    })

            self.send(
                text_data=json.dumps({
                    "studymates": studymates
                }, ensure_ascii=False)
            )

            if self.stop :
                break

            sleep(60)



    def receive(self, text_data):

        #토큰으로 user 식별하기
        headers = dict(self.scope['headers'])
        print(headers)

        token = headers[b'authorization'].decode().split(' ')[1]
        payload = jwt.decode(token, 'secret', algorithm='HS256')
        token_uid = payload['id']
        print(token_uid)

        data = json.loads(text_data)
        room_id = data['room_id']
        room_query=Room_Enroll.objects.filter(room_id=room_id)


        self.stop = False
        self.thread = threading.Thread(target=self.action(room_query, token_uid))
        self.thread.start()







