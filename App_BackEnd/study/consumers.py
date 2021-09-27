import threading
from time import sleep
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from main.models import Room_Enroll
from .models import Daily_1m_content
import jwt
from api.models import User
from main.models import Room
import asyncio

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



class sendMate(AsyncWebsocketConsumer):

    global isReceived
    global disconnected
    global me
    global user
    global room


    async def connect(self):
        global isReceived
        isReceived = False
        await self.accept()



    async def disconnect(self, code):
        global user
        global room
        global isReceived
        isReceived = True

        if Room_Enroll.objects.filter(room_id=room, user_id=user).exists():
            Room_Enroll.objects.get(room_id=room, user_id=user).delete()

        raise StopConsumer



    async def receive(self, text_data):
        global user
        global room
        global isReceived

        data = json.loads(text_data)
        room_id = data['room_id']
        uid=data['uid']
        user = User.objects.get(uid=uid)
        room = Room.objects.get(room_id=room_id)
        uid = User.objects.get(uid=uid).uid


        global me

        #만약 connected 되어잇음 isreceived=false이면
        while True:
            room = Room.objects.get(room_id=room_id)
            room_query = Room_Enroll.objects.filter(room_id=room)
            studymates = []
            for room in room_query:
                user = room.user_id

                if user.uid == uid:  # 나
                    if Daily_1m_content.objects.filter(uid=user).exists():
                        study_info = Daily_1m_content.objects.filter(uid=user)
                        concent = 0
                        play = 0


                        for info in study_info:  # 실시간 play/concent 개수 가져오기
                            if info.type == 'C':
                                concent += 1
                            elif info.type == 'P':
                                play += 1


                        concent_time = get_time(concent)
                        concent_time = concent_time.split(":")[0] + ":" + concent_time.split(":")[1]

                        play_time = get_time(play)
                        play_time = play_time.split(":")[0] + ":" + play_time.split(":")[1]

                        me = {
                            "concent_time": concent_time,
                            "play_time": play_time
                        }
                    else :
                        me = {
                            "concent_time": 0,
                            "play_time": 0
                        }



                else:  # 다른 사람들

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
                    if int(concent_time.split(":")[0]) == 0:
                        concent_time = concent_time.split(":")[1] + "분"

                    else:
                        concent_time = concent_time.split(":")[0] + "시간 " + concent_time.split(":")[1] + "분"

                    play_time = get_time(play)
                    if int(play_time.split(":")[0]) == 0:
                        play_time = play_time.split(":")[1] + "분"
                    else:
                        play_time = play_time.split(":")[0] + "시간 " + play_time.split(":")[1] + "분"

                    if user.uid != uid:
                        studymates.append({
                            "nickname": user.nickname,
                            "concent_rate": str(concent_rate) + "%",
                            "concent_time": concent_time,
                            "play_time": play_time
                        })

            await self.send(
                text_data=json.dumps({
                    "myStatus": me,
                    "studymates": studymates
                }, ensure_ascii=False)
            )

            await asyncio.sleep(10)
            print("finished")


