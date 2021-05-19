import datetime
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
from .models import Daily_1m_content, Study_analysis
from .serializers import daily_1m_serializer, study_ana_serializer


#전역변수로 버튼 초기화
start = False
stop = True

class study_button(views.APIView):

    def post(self, request):

        current_user_uid = request.data.get('uid')  # 요청한 사용자 받아오기
        user = User.objects.get(uid=current_user_uid)

        if user:
            try:
                if (request.data.get('type')=='start'):
                    start = True
                    stop = False

                else:
                    start = False
                    stop = True

                return HttpResponse(status=status.HTTP_200_OK)

            except:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        else :
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)




class study_data(views.APIView):

    def post(self, request):

        uid = request.data.get("uid")
        user = User.objects.get(uid=uid)

        time = request.data.get('time')  # char형태로 받음
        get_type = request.data.get('type')

        now = timezone.now()
        hour = now.hour

        if 0 <= hour <= 3:   # 자정 ~ 오전 4시 : 전날 모델로 생성(없을 경우)
            if not Study_analysis.objects.filter(uid=user, date=now.date()-datetime.timedelta(days=1)).exists():

                user.daily_1m_uid.all().delete()
                Study_analysis.objects.create(uid=user, date=now.date() - datetime.timedelta(days=1))

        else:  # 아니면 해당 날짜 모델로 생성(없을 경우)
            if not Study_analysis.objects.filter(uid=user, date=now.date()).exists():

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

            return Response({"tot_concent_time": final_tot_concent, "tot_play_time": final_tot_play},status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)







class ten_min_data(views.APIView):

    def get(self,request):

        Response()

    def post(self, request):

        Response()