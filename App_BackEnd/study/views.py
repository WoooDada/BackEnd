import datetime
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
from main.models import Room, Room_Enroll
from .models import Daily_1m_content, Study_analysis, One_week_study_data, today_date
from .serializers import daily_1m_serializer, study_ana_serializer
import jwt
from main.models import Recent_Room



#delete해서 Daily_1m_concent 데이터 사라지기 전에 저장. 즉, 00:00 ~ 04:00 사이의 데이터 저장하는 부분
temp_list =[]
member_array =[]
global isFinished

class inout(views.APIView):

    #룸 입장
    def post(self,request):
        global isFinished
        isFinished = False

        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])

        get_room_id = request.data.get("room_id")

        room = Room.objects.get(room_id=get_room_id)

        if Room_Enroll.objects.filter(room_id=room, user_id=user).exists():
            Room_Enroll.objects.get(room_id=room, user_id=user).delete()
            if [room.room_id, user.uid] in member_array :
                member_array.remove([room.room_id, user.uid])


        if [room.room_id, user.uid] not in member_array:

            #최근 방에 저장하기
            recent_room = Recent_Room.objects.create(
                room_array = room,
                user_id=user
            )
            recent_room.save()

            #현재활동중 표시 위해
            room_enroll = Room_Enroll.objects.create(
                room_id=room,
                user_id = user,
                current = True,
                room_color = room.room_color
            )
            room_enroll.save()
            member_array.append([room.room_id, user.uid])

        isFinished=True


        return HttpResponse(status=status.HTTP_200_OK)


    #룸 퇴장
    def delete(self, request):

        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])

        get_room_id = request.data.get("room_id")

        room = Room.objects.get(room_id=get_room_id)
        Room_Enroll.objects.get(room_id=room, user_id=user).delete()
        member_array.remove([room.room_id, user.uid])


        return HttpResponse(status=status.HTTP_200_OK)




class study_data(views.APIView):


    def week_time(self,user):

        query_set = user.daily_1m_uid.all()
        tot_con_time = 0
        tot_play_tme = 0

        for qs in query_set:

            if qs.type == 'C':
                tot_con_time = tot_con_time + 1

            elif qs.type == 'P':
                tot_play_tme = tot_play_tme + 1

        return {"concent":tot_con_time, "play":tot_play_tme}


    def post(self, request):


        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])

        time = request.data.get('time')  # char형태로 받음
        get_type = request.data.get('type')

        now = timezone.now()
        hour = now.hour
        day = now.today().weekday()
        days =['일','월','화','수','목','금','토']

        if not today_date.objects.filter(uid=user, day=now.date()).exists() :
            today_date.objects.create(uid=user, day=now.date())

        count_today_date = user.today_date_uid.count()
        today_query_set = user.today_date_uid.all()

        if count_today_date == 7 :
            today_query_set[0].delete()
        if One_week_study_data.objects.count() == 7:
            qs = One_week_study_data.objects.all()
            qs[0].delete()  #가장 오래된 객체 삭제하여 7개 유지


        if 0 <= hour <= 3:   # 자정 ~ 오전 4시 : 전날 모델로 생성(없을 경우)

            if not Study_analysis.objects.filter(uid=user, date=now.date()-datetime.timedelta(days=1)).exists():

                week_time = self.week_time(user)
                if count_today_date != 1:
                    if today_query_set[count_today_date - 2].day == now.date() - datetime.timedelta(days=1):
                        One_week_study_data.objects.create(uid=user, day=now.date() - datetime.timedelta(days=1),
                                                        date=days[day], concent_time=week_time['concent'] ,
                                                       play_time= week_time['play'])      #삭제 전 데이터 생성


                user.daily_1m_uid.all().delete()
                Study_analysis.objects.create(uid=user, date=now.date() - datetime.timedelta(days=1))

        else:  # 아니면 해당 날짜 모델로 생성(없을 경우)
            if not Study_analysis.objects.filter(uid=user, date=now.date()).exists():


                #temp_list = get_tenmin_data(user, -1, -1, 2) # 00:00 ~ 4:00 10분단위 데이터 저장
                week_time = self.week_time(user)
                if count_today_date != 1 :
                    if today_query_set[count_today_date - 2].day == now.date() - datetime.timedelta(days=1):
                        One_week_study_data.objects.create(uid=user, day=now.date() - datetime.timedelta(days=1),
                                                    date=days[day], concent_time=week_time['concent'],
                                                    play_time=week_time['play'])  # 삭제 전 데이터 생성

                user.daily_1m_uid.all().delete()
                Study_analysis.objects.create(uid=user, date=now.date())


        serializer = daily_1m_serializer(data=request.data,instance=user)

        if serializer.is_valid():
            serializer.save()
            Daily_1m_content.objects.create(uid=user, type=get_type, time=time)




        qs = Study_analysis.objects.filter(uid=user).values_list('uid','daily_tot_hour','daily_concent_hour','date')
        count = Study_analysis.objects.filter(uid=user).count() - 1
        study_data = {

            'uid':qs[count][0],
            'daily_tot_hour':qs[count][1],
            'daily_concent_hour':qs[count][2],
            'date':qs[count][3]

        }


        serializer_2 = study_ana_serializer(data=study_data, instance=user)

        if serializer_2.is_valid() :

            serializer_2.save()

            tot_time = int(qs[count][1])
            tot_con = int(qs[count][2])
            obj = Study_analysis.objects.filter(uid=user).last()

            if get_type == 'C':
                tot_con += 1
            tot_time += 1


            obj.daily_tot_hour = str(tot_time)
            obj.daily_concent_hour = str(tot_con)
            obj.save()

            total_play_time = tot_time - tot_con

            if get_type == 'U':
                total_play_time = total_play_time-1

            tot_play_hour = total_play_time // 60
            tot_play_minute = total_play_time - tot_play_hour*60

            tot_concent_hour = tot_con // 60
            tot_concent_minute = tot_con - tot_concent_hour * 60

            if tot_concent_minute // 10 == 0:
                tot_concent_minute = "0"+str(tot_concent_minute)

            if tot_play_minute // 10 == 0:
                tot_play_minute = "0"+str(tot_play_minute)

            final_tot_play = str(tot_play_hour) + ':' + str(tot_play_minute)
            final_tot_concent = str(tot_concent_hour) + ':' + str(tot_concent_minute)

            return Response({"tot_concent_time": final_tot_concent,
                             "tot_play_time": final_tot_play},
                            status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)






class ten_min_data(views.APIView):

    def get_tenmin_data(self, user, hour, minute, get_type):

        one_min_list = []
        whole_min_list = []

        query_set = user.daily_1m_uid.all()
        #   type_array = []     # length = 10인 배열로 C / P / U 들어감

        hour_array = [
            '00','01','02','03','04','05','06','07','08','09','10','11','12','13','14',
            '15','16','17','18','19','20','21','22','23'
        ]  # hour와 같은 시간인 data 있는 배열

        minute_array = ['00','10','20','30','40','50']


        whole_hour = [
            [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        ]


        if 0<=hour<=9 :
            hour_str = str(0) + str(hour) + ":" + str(minute - 1)  # 0~9시인경우 00~09시로 변경

        else :
            hour_str = str(hour) + ":" + str(minute - 1)

        for qs in query_set:

            qs_data = {
                "stt_time": qs.time,
                "end_time": qs.time,
                "concent_type": qs.type
            }


            if qs.time == hour_str :
                one_min_list.append(qs_data)

            qs_hour = qs.time.split(":")[0]         #hour 잘라내기

            flag = 0
            for h in hour_array :    #whole_hour 2차원 배열에 같은 hour끼리 넣기
                if h == qs_hour :
                    whole_hour[flag].append(qs)
                    break
                flag = flag  + 1


        if get_type == 0:  # 해당되는 1분 데이터 주기 5/25 2:17에 get인 경우 5/24 2:16 데이터 넘기기
            return qs_data


        elif get_type == 1:  # 해당 날짜의 모든 데이터 가져오기

            hour_tag = 0

            for w in whole_hour:
                whole_minute = [
                    [], [], [], [], [], []
                ]  # 순서대로 00~09 / 10~19 / ... / 50 ~59 분에 해당하는 type 들어가는 배열

                now_hour = hour_array[hour_tag]
                hour_tag = hour_tag + 1
                if w == []:
                    continue

                for h in w :
                    h_minute = h.time.split(":")[1]      #쿼리셋객체 하나의 minute 잘라오기
                    h_minute = h_minute[0]          #쿼리셋객체 minute의 앞자리
                    whole_minute[int(h_minute)].append(h.type)

                minute_tag = 0
                for a in whole_minute :

                    check_concent = 0  # 10분 중 'C'갯수
                    check_play = 0  # 10분 중 'P'갯수

                    temp_tag = minute_tag
                    minute_tag = minute_tag + 1

                    if a == [] :
                        continue

                    for type in a :
                        if type == 'C' :
                            check_concent = check_concent + 1
                        elif type == 'P':
                            check_play = check_play + 1


                    stt_time = now_hour + ":" + minute_array[temp_tag]    #stt_time
                    now_minute = minute_array[temp_tag]
                    end_minute = str(now_minute[0]) + "9"
                    end_time = now_hour + ":" + end_minute      #end_time


#1분에 3개씩 -> 10분 30개이므로 과반수인 15가 c면 c리턴
                    if check_concent > check_play and (check_concent + check_play) >= 15 :
                        concent_type = 'C'
                        qs_data = {
                            "stt_time": stt_time,
                            "end_time": end_time,
                            "concent_type": concent_type
                        }
                        whole_min_list.append(qs_data)
                    elif check_concent <= check_play and (check_concent + check_play) >= 15 :
                        concent_type = 'P'

                        qs_data = {
                            "stt_time": stt_time,
                            "end_time": end_time,
                            "concent_type": concent_type
                        }
                        whole_min_list.append(qs_data)

            return whole_min_list




    def get(self,request):

     #   current_user_uid = self.request.query_params.get('uid')  # 요청한 사용자 받아오기

        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])


     #   user = User.objects.get(uid=current_user_uid)[0]

        update = self.request.query_params.get("update")

        now = timezone.now()
        minute = now.minute
        hour = now.hour

        if update == 'F' :  #홈 -> 공부 : 이전 데이터 한번에

            ten_data = self.get_tenmin_data(user, hour, minute, 1)
            return Response({"ten_min_list": ten_data}, status=status.HTTP_200_OK)


        elif update == 'T' :  #현재 실시간 공부중, 1분마다 get

            ten_data = self.get_tenmin_data(user, hour, minute, 0)

            return Response({"ten_min_list":ten_data},status=status.HTTP_200_OK)

        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)


class room_info(views.APIView):

    def get(self, request):

        global isFinished
        isFinished = False

        while not isFinished :
            if isFinished :
                break

        room_id = self.request.query_params.get("room_id")
        room = Room.objects.get(room_id=room_id)
        response = {
            "room_name":room.room_name,
            "room_tag":room.room_tag,
            "in_ppl":Room_Enroll.objects.filter(room_id=room).count(),
            "max_ppl":room.maxppl,
            "room_manner":room.room_comment,
            "room_issecret":room.is_secret
        }

        return Response(response,status=status.HTTP_200_OK)


