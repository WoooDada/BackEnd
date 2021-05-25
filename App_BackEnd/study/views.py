import datetime
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
from .models import Daily_1m_content, Study_analysis, One_week_study_data
from .serializers import daily_1m_serializer, study_ana_serializer


#delete해서 Daily_1m_concent 데이터 사라지기 전에 저장. 즉, 00:00 ~ 04:00 사이의 데이터 저장하는 부분
temp_list =[]

#전역변수로 버튼 초기화
start = False
stop = True
#start = True                       #ten_min_data 'local로' test할때 바꿔주고 해!!
#stop = False



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

        uid = request.data.get("uid")
        user = User.objects.get(uid=uid)

        time = request.data.get('time')  # char형태로 받음
        get_type = request.data.get('type')

        now = timezone.now()
        hour = now.hour
        day = now.today().weekday()
        days =['일','월','화','수','목','금','토']


        if One_week_study_data.objects.count() == 7:
            qs = One_week_study_data.objects.all()
            qs[0].delete()  #가장 오래된 객체 삭제하여 7개 유지


        if 0 <= hour <= 3:   # 자정 ~ 오전 4시 : 전날 모델로 생성(없을 경우)
            if not Study_analysis.objects.filter(uid=user, date=now.date()-datetime.timedelta(days=1)).exists():

                week_time = self.week_time(user)
                One_week_study_data.objects.create(uid=user, date=days[day], concent_time=week_time['concent'] ,
                                                   play_time= week_time['play'])      #삭제 전 데이터 생성

                user.daily_1m_uid.all().delete()
                Study_analysis.objects.create(uid=user, date=now.date() - datetime.timedelta(days=1))

        else:  # 아니면 해당 날짜 모델로 생성(없을 경우)
            if not Study_analysis.objects.filter(uid=user, date=now.date()).exists():


                #temp_list = get_tenmin_data(user, -1, -1, 2) # 00:00 ~ 4:00 10분단위 데이터 저장
                week_time = self.week_time(user)
                One_week_study_data.objects.create(uid=user, date=days[day], concent_time=week_time['concent'],
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

            return Response({"tot_concent_time": final_tot_concent, "tot_play_time": final_tot_play},status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)






class ten_min_data(views.APIView):

    def get_tenmin_data(self, user, hour, minute, get_type):

        one_min_list = []
        whole_min_list = []

        query_set = user.daily_1m_uid.all()
        #   type_array = []     # length = 10인 배열로 C / P / U 들어감

        hour_array = []  # hour와 같은 시간인 data 있는 배열
        final_array = []  # 시간 만족하는 data들 들어가는 final_array로 최대 길이 10
        # hour_array의 배열 중 해당되는 minute data 있는 배열

        data_length = 0
        #hour_str = str(hour) + ":" +str(minute)
        hour_str = str(0) + str(hour) + ":" + str(minute-1)  # 00~03시인경우

        for qs in query_set:

            qs_data = {
                "stt_time": qs.time,
                "end_time": qs.time,
                "concent_type": qs.type
            }

            whole_min_list.append(qs_data)

            if qs.time == hour_str :
                one_min_list.append(qs_data)

            """
            qs_hour = qs.time.split(":")[0]
            if qs_hour[0] == 0:
                qs_hour = qs_hour[1]

            if qs_hour == hour:
                hour_array.append(qs)  # 같은 시간인 data 넣기
                  """

        if get_type == 0:  # 해당되는 1분 데이터 주기 5/25 2:17에 get인 경우 5/24 2:16 데이터 넘기기

            """
            for qs in hour_array:
                qs_minute = qs.time.split(":")[1]
                if qs_minute == minute - 1:
                    data = {
                        "stt_time": qs.time,
                    "end_time": qs.time,
                    "concent_type": qs.type
                    }

                    one_min_list.append(data)
                    return one_min_list
"""
            return one_min_list

        elif get_type == 1:  # 해당 날짜의 모든 데이터 가져오기
            return whole_min_list

        """
        for qs in hour_array :        #같은 시간대 qs_array 중 해당되는 minute 찾기
            qs_minute = qs['time'].split(":")[1]
            qs_minute = qs_minute[0]    #존재하는 data들의 십의자리 minute 가져오기

            temp_minute = minute[0] - 1     #받아온 minute을 십의자리만 가져와서 1빼줌


            if temp_minute == -1 :
                temp_minute = 5     #-1인 경우 (즉, minute == 0일때,  50분~59분인 경우이므로 5로 만들어주기)

            if qs_minute == temp_minute :
                final_array.append(qs)              #객체 추가
                type_array.append(qs['type'])       #type넣기('C' / 'P' / 'U')
                data_length = data_length + 1       #type/final array의 length

        start_time = final_array[0]['time']
        end_time = final_array[len(final_array)-1]['time']
        type_concent = 0
       """

    #  if hour == -1 and minute == -1 and get_type == 2 : #00:00 ~ 4:00 10분단위 데이터 저장

    def get(self,request):

        current_user_uid = self.request.query_params.get('uid')  # 요청한 사용자 받아오기
        user = User.objects.get(uid=current_user_uid)

        update = request.data.get("update")

        now = timezone.now()
        minute = now.minute
        hour = now.hour

        if update == 'F' :  #홈 -> 공부 : 이전 데이터 한번에

           # if start == True and stop == False:         #temp_list의 00:00 ~ 4:00 데이터와 해당날짜의 나머지꺼 합쳐주기

                ten_data = self.get_tenmin_data(user, hour, minute, 1)

                return Response({"ten_min_list:": ten_data}, status=status.HTTP_200_OK)

          #  else :
           #     return Response(status=status.HTTP_400_BAD_REQUEST)

        elif update == 'T' :  #현재 실시간 공부중, 1분마다 get

         #   if start == True and stop == False:

                ten_data = self.get_tenmin_data(user, hour, minute, 0)

         #       return Response({"ten_min_list:":ten_data},status=status.HTTP_200_OK)

          #  else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)
