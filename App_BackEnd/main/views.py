from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework import views, status
from api.models import User
from study.models import Study_analysis


now = timezone.now()
hour = now.hour
if 0 <= hour <= 3:
    date = now.date()-datetime.timedelta(days=1)
else :
    date = now.date()


class studyrank(views.APIView):

    def get(self, request):
        try :
            rank_study_list = []

            uid = self.request.query_params.get('uid')
            my_nickname = User.objects.get(uid=uid)
            my_study_data = Study_analysis.objects.get(uid = uid)

            study_queryset = Study_analysis.objects.filter(date=date).order_by('-daily_concent_hour')
                    # 집중시간 순서로 내림차순 정렬
            num = 1
            my_rank_num = 0

            for my_rank in study_queryset :  # 내 랭킹 찾기
                if uid == my_rank.uid.uid:
                    my_rank_num = num

                    if my_study_data.daily_concent_hour < 60 :
                        hour = 0
                    else :
                        hour = my_study_data.daily_concent_hour / 60
                    minute = my_study_data.daily_concent_hour - hour * 60
                    if minute < 10:
                        minute = "0" + str(minute)
                    time_string = str(hour) + ":" + str(minute)

                    rank_study_list.append({  # 내 데이터 넣기
                        'rank': my_rank_num,
                        'nickname': my_nickname.nickname,
                        'tot_concent_time': time_string
                    })

                    break
                else :
                    num += 1



            prev_concent_time = 0
            rank = 0
            count = 0

            for study in study_queryset:        #상위 10명 데이터 리스트에 넣기

                uid = study.uid
                nickname = User.objects.get(uid=uid).nickname

                my_concent_time = study.daily_concent_hour
                if prev_concent_time == my_concent_time:    #전 사람과 동점
                    count += 1

                else :

                    if count > 10 :
                        break

                    count += 1
                    rank = rank + 1


                prev_concent_time = my_concent_time

                if study.daily_concent_hour < 60:
                    hour = 0
                else:
                    hour = study.daily_concent_hour / 60
                minute = study.daily_concent_hour - hour * 60
                if minute < 10 :
                    minute = "0" + str(minute)
                time_string = str(hour) + ":" + str(minute)

                rank_study_list.append({
                    'rank' : rank,
                    'nickname' : nickname,
                    'tot_concent_time' : time_string
                })

            return Response({'rank_study_list':rank_study_list}, status=status.HTTP_200_OK)
        except:
            return Response({'message' : "fail"},status=status.HTTP_400_BAD_REQUEST)



class playrank(views.APIView):

    def get(self, request):

        try :
            rank_study_list = []

            uid = self.request.query_params.get('uid')
            my_nickname = User.objects.get(uid=uid)
            my_study_data = Study_analysis.objects.get(uid=uid)



        except:
            return Response({'message' : "fail"},status=status.HTTP_400_BAD_REQUEST)

class random_rooms(views.APIView):

    def get(self, request):

        return


class my_rooms(views.APIView):

    def get(self, request):

        return