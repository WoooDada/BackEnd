
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
from study.models import One_week_study_data, Daily_1m_content
import datetime


class badge_profile(views.APIView):

    def get(self,request):
        current_user_uid = self.request.query_params.get('uid')
        user = User.objects.get(uid=current_user_uid)


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
        current_user_uid = self.request.query_params.get('uid')  # 요청한 사용자 받아오기
        user = User.objects.get(uid=current_user_uid)

        now = timezone.now()
        date = now.date()   #오늘 날짜

        date_array = []
        day_array = []
        count = 0

        days = ['월', '화', '수', '목', '금', '토','일']
        for i in range(1,8):     #어제부터 1주일 전까지 날짜 들어간 배열 date_array 생성
            a = date - datetime.timedelta(days=i)
            date_array.append(a)
            day_array.append(days[a.weekday()])

        if user:

            query_set = One_week_study_data.objects.filter(uid=user)

            for k in date_array :

                flag = False

                for qs in query_set :

                    if k == qs.day :

                        data_set = {
                            "date": qs.date,
                            "concent_time": qs.concent_time,
                            "play_time": qs.play_time
                        }
                        flag= True
                        count = count + 1
                        graph.append(data_set)
                        break

                if flag == False :

                    data_set = {
                        "date" : day_array[count],
                        "concent_time": 0,
                        "play_time":0
                    }

                    count = count + 1
                    graph.append(data_set)
                    graph.reverse()


            return JsonResponse({"graph":graph}, safe=False, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii': False})
        else :
            return JsonResponse({"message": "no uid"}, status=status.HTTP_400_BAD_REQUEST)


class today_concent(views.APIView):

    def get(self, request):

        try :
            current_user_uid = self.request.query_params.get('uid')  # 요청한 사용자 받아오기
            user = User.objects.get(uid=current_user_uid)

            query_set = user.daily_1m_uid.all()
            tot_con_time = 0

            for qs in query_set:

                if qs.type == 'C':
                    tot_con_time = tot_con_time + 1

            tot_time = user.daily_1m_uid.count()
            play_time = tot_time - tot_con_time

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

            return Response({"tot_concent_rate":concent_rate,
                             "tot_concent_time": final_tot_concent,
                             "tot_time": final_tot_time,
                             "tot_play_time" : final_play_time
                             },
                            status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


