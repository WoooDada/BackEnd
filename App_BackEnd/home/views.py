
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
from study.models import One_week_study_data, Daily_1m_content
import datetime
import jwt

class badge_profile(views.APIView):

    def get(self,request):

        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])
     #   current_user_uid = self.request.query_params.get('uid')
      #  user = User.objects.get(uid=current_user_uid)


        if user:
            uid = user.uid
            nickname = user.nickname
            badge = user.badge

            return JsonResponse({"nickname": nickname, "badge": badge},  json_dumps_params={'ensure_ascii': False},
                                status=status.HTTP_200_OK)

        else :
            return JsonResponse({"message": "no uid"}, status=status.HTTP_400_BAD_REQUEST)



class concent_graph(views.APIView):


    def get(self,request):

        """
        study/models의 One_week_study 모델 사용
        study/views의 study_data 클래스에서 week_time 함수 사용해
        매일 daily_concent_data 객체들 사라지기 전에 create 해줌
        One_week_study의 객체 수는 항상 7개 이하로 유지 (7일 데이터여서)
        """

        graph = []

        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])

       # current_user_uid = self.request.query_params.get('uid')  # 요청한 사용자 받아오기
       # user = User.objects.get(uid=current_user_uid)

        now = timezone.now()
        date = now.date()   #오늘 날짜

        date_array = []
        day_array = []
        count = 0


        day_list = ['월', '화', '수', '목', '금', '토', '일']
        today = day_list[datetime.datetime.today().weekday()]  # 오늘 요일

        list = []
        if today == '월' : list = ['화', '수', '목', '금', '토', '일','월']
        elif today=='화' : list = ['수', '목', '금', '토', '일','월', '화']
        elif today=='수' : list = ['목', '금', '토', '일','월', '화', '수']
        elif today=='목' : list = ['금', '토', '일','월', '화', '수','목']
        elif today=='금': list = ['토', '일','월', '화', '수', '목', '금']
        elif today=='토' : list = ['일','월', '화', '수', '목', '금', '토']
        elif today=='일' : list = ['월', '화', '수', '목', '금', '토', '일']

        if One_week_study_data.objects.filter(uid=user).exists():
            query_set = One_week_study_data.objects.filter(uid=user)

            for day in list :
                flag = False
                count = 0
                for qs in query_set:
                    if day[count] == qs.date :

                        data_set = {
                            "date": qs.date,
                            "concent_time": qs.concent_time,
                            "play_time": qs.play_time
                        }
                        count += 1
                        flag = True
                        graph.append(data_set)
                        break
                if flag is False  :
                    data_set = {
                        "date": day_list[count],
                        "concent_time": 0,
                        "play_time": 0
                    }
                    count = count + 1
                    graph.append(data_set)


            return JsonResponse({"graph":graph}, safe=False, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii': False})
        else :


            for i in list :
                data_set = {
                    "date": i,
                    "concent_time": 0,
                    "play_time": 0
                }
                graph.append(data_set)
            print(graph)
            return JsonResponse({"graph":graph},status=status.HTTP_200_OK)


class today_concent(views.APIView):

    def get(self, request):

        try :

            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])


   #         current_user_uid = self.request.query_params.get('uid')  # 요청한 사용자 받아오기
    #        user = User.objects.get(uid=current_user_uid)


            query_set = user.daily_1m_uid.all()
            tot_con_time = 0

            for qs in query_set:

                if qs.type == 'C':
                    tot_con_time = tot_con_time + 1

            tot_time = user.daily_1m_uid.count()
            print(tot_time)
            print(tot_con_time)
            play_time = tot_time - tot_con_time
            print(play_time)
            concent_rate = round(tot_con_time / tot_time * 100, 1)

            tot_concent_hour = tot_con_time // 60
            tot_concent_minute = tot_con_time - tot_concent_hour * 60

            tot_time_hour = tot_time // 60
            tot_time_minute = tot_time - tot_time_hour * 60

            tot_play_hour = play_time // 60
            tot_play_minute = play_time - tot_play_hour * 60

            if tot_concent_minute // 10 == 0:
                tot_concent_minute = "0"+str(tot_concent_minute)

            if tot_time_minute // 10 == 0:
                tot_time_minute = "0"+str(tot_time_minute)

            if tot_play_minute // 10 == 0:
                tot_play_minute = "0"+str(tot_play_minute)

            final_tot_concent = str(tot_concent_hour) + ':' + str(tot_concent_minute)
            final_tot_time = str(tot_time_hour) + ':' + str(tot_time_minute)
            final_play_time = str(tot_play_hour) + ":" + str(tot_play_minute)
            print(final_play_time)
            return Response({"tot_concent_rate":concent_rate,
                             "tot_concent_time": final_tot_concent,
                             "tot_time": final_tot_time,
                             "tot_play_time" : final_play_time
                             },
                            status=status.HTTP_200_OK)

        except:
            return Response({"tot_concent_rate":"0",
                             "tot_concent_time": "00:00",
                             "tot_time": "00:00",
                             "tot_play_time" : "00:00",
                             },
                            status=status.HTTP_200_OK)


