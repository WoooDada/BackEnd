from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework import views, status
from api.models import User
from study.models import Study_analysis
from .models import Room, Room_Enroll


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
            prev_mystudy=0
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
                else:
                    num += 1
                prev_mystudy = my_rank.daily_concent_hour


            prev_concent_time = 0
            rank = 0
            count = 0
            flag = False
            prev_rank = 0
            for study in study_queryset:        #상위 10명 데이터 리스트에 넣기

                uid = study.uid
                nickname = User.objects.get(uid=uid).nickname

                my_concent_time = study.daily_concent_hour

                if study.daily_concent_hour < 60:
                    hour = 0
                else:
                    hour = study.daily_concent_hour / 60
                minute = study.daily_concent_hour - hour * 60
                if minute < 10 :
                    minute = "0" + str(minute)
                time_string = str(hour) + ":" + str(minute)

                if prev_concent_time == my_concent_time:    #전 사람과 동점
                    count += 1


                    rank_study_list.append({
                        'rank': prev_rank,
                        'nickname': nickname,
                        'tot_concent_time': time_string,
                        'prev': prev_concent_time
                    })

                else :

                    count += 1
                    rank += 1
                    prev_rank = count
                    if count > 10 :
                        break

                    rank_study_list.append({
                        'rank': count,
                        'nickname': nickname,
                        'tot_concent_time': time_string,
                        'prev': prev_concent_time
                    })



                prev_concent_time = my_concent_time


            return Response({'rank_study_list':rank_study_list}, status=status.HTTP_200_OK)
        except:
            return Response({'message' : "fail"},status=status.HTTP_400_BAD_REQUEST)



class playrank(views.APIView):

    def get(self, request):

        try :
            rank_play_list = []

            uid = self.request.query_params.get('uid')
            my_nickname = User.objects.get(uid=uid).nickname
            my_study_data = Study_analysis.objects.get(uid=uid).daily_tot_hour - Study_analysis.objects.get(uid=uid).daily_concent_hour

            study_query = Study_analysis.objects.filter(date=date)

            play_dict = {}
            for ppl in study_query :
                nickname = User.objects.get(uid=ppl.uid).nickname
                play_rate = round(ppl.daily_concent_hour / ppl.daily_tot_hour * 100,2)
                play_dict[nickname] = play_rate

            play_dict = sorted(play_dict.items(), key=lambda x: x[1], reverse=True)         #play_hour 순서로 내림차순 정렬

            #내 순위 찾기
            my_rank = 1
            prev_playtime = 0
            prev_rank = 0
            for key in play_dict:
                if key[0] == my_nickname :
                    my_rate = str(key[1]) + "%"
                    rank_play_list.append({
                        'rank': my_rank,
                        'nickname': my_nickname,
                        'tot_concent_rate': my_rate
                    })
                    break
                else:
                    my_rank += 1
                prev_playtime = key[1]

         #   print(play_dict)
            #상위 10명 뽑기
            num = 0
            rank_10 = 0
            prev_rate = 0.0
            for key in play_dict:
                if key[1] == prev_rate :        #같으면 rank전과 동일하고 num만 늘어남

                    num += 1
                    rank_play_list.append({
                        'rank': prev_rank,
                        'nickname': key[0],
                        'tot_concent_rate': str(key[1]) + "%"
                    })
                else :
                    #if num > 10 :
                     #   break
                    num += 1
                    rank_10 += 1
                    prev_rank = num
                    if num > 10 :
                        break

                    rank_play_list.append({
                        'rank': num,
                        'nickname': key[0],
                        'tot_concent_rate': str(key[1]) + "%"
                    })

                prev_rate = key[1]



            return Response({'rank_play_list': rank_play_list}, status=status.HTTP_200_OK)
            #return Response({'rank_play_list': play_dict}, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            return Response({'message' : "fail"}, status=status.HTTP_400_BAD_REQUEST)

class random_rooms(views.APIView):

    def get(self, request):



        return


class my_rooms(views.APIView):

    def get(self, request):
        my_room_list = []
        num = 0
        try:
            uid = self.request.query_params.get('uid')
            user = User.objects.get(uid=uid)
            myroom_queryset = user.f_uid.all()

            for query in myroom_queryset:

                room = query.room_id
                num = Room_Enroll.objects.filter(room_id=room).count()
                my_room_list.append({
                    'room_id':room.room_id,
                    'room_name':room.room_name,
                    'inppl': num,
                    'maxppl' : room.maxppl,
                    'room_color':room.room_color
                })
            return Response({'my_room_list': my_room_list}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message' : "fail"}, status=status.HTTP_400_BAD_REQUEST)