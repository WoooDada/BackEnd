import random
from django.utils import timezone
import datetime
from rest_framework.response import Response
from rest_framework import views, status
from api.models import User
from study.models import Study_analysis,Daily_1m_content
from .models import Room, Room_Enroll
import jwt

now = timezone.now()
hour = now.hour
if 0 <= hour <= 3:
    date = now.date()-datetime.timedelta(days=1)
else :
    date = now.date()



def get_time(count):

    hour = count // 60
    minute = count - hour * 60

    if minute < 10:
        minute = "0" + str(minute)
    time_string = str(hour) + ":" + str(minute)
    return time_string



class studyrank(views.APIView):

    def get(self, request):
        try :
            total_num = 0
            rank_study_list = []

            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

          #  uid = self.request.query_params.get('uid')
            uid = user.uid
            my_nickname = user


            user_query = User.objects.all()
            study_list = []

            for user in user_query:
                sub_list = []
                if Daily_1m_content.objects.filter(uid=user.uid).exists():
                    user_1m_data_query = Daily_1m_content.objects.filter(uid=user.uid)
                    concent = 0

                   # tot_count = user_1m_data_query.count()
                 #   if tot_count != 0:   # 오늘 안들어온 사람은 쿼리에 추가 x
                    for one_min in user_1m_data_query:  # c / p 개수 세기
                        if one_min.type == 'C':
                            concent += 1

                    sub_list.append(user)
                    sub_list.append(concent)
                    study_list.append(sub_list)     #study_list에 [user, tot_concent] 추가
                else :
                    concent = 0
                    sub_list.append(user)
                    sub_list.append(concent)
                    study_list.append(sub_list)

            """

            if len(study_list) == 0:
                rank_study_list.append({
                    'rank': 1,
                    'nickname': my_nickname.nickname,
                    'tot_concent_time': '0:00',

                })
                return Response({'rank_study_list': rank_study_list}, status=status.HTTP_200_OK)
            """
            study_list.sort(key=lambda x:-x[1])   #tot_concent 순서로 정렬

            num=1
            #내 랭킹 찾기
            for user_info in study_list:
                user = user_info[0]
                concent_time = user_info[1]

                if user.uid == my_nickname.uid :
                    my_rank_num = num
                    time_string = get_time(concent_time)

                    rank_study_list.append({  # 내 데이터 넣기
                        'rank': my_rank_num,
                        'nickname': my_nickname.nickname,
                        'tot_concent_time': time_string
                    })
                   # print("num:"+num)
                    break
                else:
                    num += 1

            #상위 10명 찾기
            prev_concent_time = 0
            rank = 0
            count = 0
            prev_rank = 0

            for study in study_list:  # 상위 10명 데이터 리스트에 넣기

                uid = study[0].uid
                nickname = User.objects.get(uid=uid).nickname

                my_concent_time = study[1]
                time_string=get_time(my_concent_time)

                if prev_concent_time == my_concent_time:  # 전 사람과 동점
                    if count > 10:
                        break

                    count += 1

                    rank_study_list.append({
                        'rank': prev_rank,
                        'nickname': nickname,
                        'tot_concent_time': time_string,
                       # 'prev': prev_concent_time
                    })

                else:

                    if count > 10:
                        break

                    count += 1
                    rank += 1
                    prev_rank = count

                    rank_study_list.append({
                        'rank': count,
                        'nickname': nickname,
                        'tot_concent_time': time_string,
                   #     'prev': prev_concent_time
                    })

                prev_concent_time = my_concent_time

            return Response({'rank_study_list': rank_study_list}, status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({'message' : "fail"},status=status.HTTP_400_BAD_REQUEST)



class playrank(views.APIView):

    def get(self, request):

        try :
            rank_play_list = []

            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

        #    uid = self.request.query_params.get('uid')
            my_nickname = User.objects.get(uid=user.uid)

            user_query = User.objects.all()
            study_list = []
            for user in user_query:
                sub_list = []
                if Daily_1m_content.objects.filter(uid=user.uid).exists():
                    user_1m_data_query = Daily_1m_content.objects.filter(uid=user.uid)
                    concent = 0

                    tot_count = user_1m_data_query.count()
                    if tot_count != 0:  # 오늘 안들어온 사람은 쿼리에 추가 x
                        for one_min in user_1m_data_query:  # c / p 개수 세기
                            if one_min.type == 'C':
                                concent += 1
                        concent_rate = concent / tot_count * 100
                        sub_list.append(user)
                        sub_list.append(concent_rate)
                        study_list.append(sub_list)  # study_list에 [user, concent_rate] 추가
                else :
                    sub_list = []
                    concent_rate= 0.0
                    sub_list.append(user)
                    sub_list.append(concent_rate)
                    study_list.append(sub_list)  # study_list에 [user, concent_rate] 추가


            """
            if len(study_list) == 0:
                rank_play_list.append({
                    'rank': 1,
                    'nickname': my_nickname.nickname,
                     'tot_concent_rate': "0%"

                })
                return Response({'rank_play_list': rank_play_list}, status=status.HTTP_200_OK)
            """
            study_list.sort(key=lambda x: x[1])  # concent_rate 순서로 오름차순 정렬

            num = 1
            # 내 랭킹 찾기
            for user_info in study_list:
                user = user_info[0]
                concent_rate = user_info[1]

                if user.uid == my_nickname.uid:
                    my_rank_num = num

                    rank_play_list.append({  # 내 데이터 넣기
                        'rank': my_rank_num,
                        'nickname': my_nickname.nickname,
                        'tot_concent_rate': str(round(concent_rate,2)) + "%"
                    })
                    break
                else:
                    num += 1

            # 상위 10명 찾기
            prev_concent_time = 0
            rank = 0
            count = 0
            prev_rank = 0

            for study in study_list:  # 상위 10명 데이터 리스트에 넣기

                uid = study[0].uid
                nickname = User.objects.get(uid=uid).nickname

                my_concent_rate = study[1]

                if prev_concent_time == my_concent_rate:  # 전 사람과 동점
                    count += 1
                    if count > 10:
                        break

                    rank_play_list.append({
                        'rank': prev_rank,
                        'nickname': nickname,
                        'tot_concent_rate': str(round(my_concent_rate,2)) + "%"
                        # 'prev': prev_concent_time
                    })

                else:

                    count += 1
                    rank += 1
                    prev_rank = count
                    if count > 10:
                        break

                    rank_play_list.append({
                        'rank': count,
                        'nickname': nickname,
                        'tot_concent_rate': str(round(my_concent_rate,2)) + "%"
                        #     'prev': prev_concent_time
                    })

                prev_concent_time = my_concent_rate

            return Response({'rank_play_list': rank_play_list}, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
            return Response({'message' : "fail"}, status=status.HTTP_400_BAD_REQUEST)

class random_rooms(views.APIView):

    def get(self, request):
        all_room_list = []
        try:
            room_number = Room.objects.all().count()
            room_id_list = []
            room_not_list=[]
            num = 0

            while True:

                random_number = random.randint(1,Room.objects.all().count())

                try:
                    room = Room.objects.get(room_id=random_number)
                except:
                    continue


                room_inppl = room.f_room.all().count()
                if room_inppl >= 1:

                    if random_number in room_id_list:
                      #  room_not_list.append(random_number)
                        continue
                    else:
                        if num >= 9 :
                            break
                        num += 1
                        room_id_list.append(random_number)
                        this_room = Room.objects.get(room_id=random_number)
                        inppl =Room_Enroll.objects.filter(room_id=this_room).count()
                        all_room_list.append({
                            'room_id': this_room.room_id,
                            'room_name': this_room.room_name,
                            'inppl': inppl,
                            'maxppl': this_room.maxppl,
                            'room_color': this_room.room_color,
                            'is_secret':this_room.is_secret
                        })

            return Response({'all_room_list': all_room_list}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message' : "fail"}, status=status.HTTP_400_BAD_REQUEST)

class my_rooms(views.APIView):

    def get(self, request):
        my_room_list = []
        num = 0
        try:

            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

            myroom_queryset = user.f_uid.all().order_by('-room_id')[:10]

            for query in myroom_queryset:

                room = query.room_id
                num = Room_Enroll.objects.filter(room_id=room).count()
                my_room_list.append({
                    'room_id':room.room_id,
                    'room_name':room.room_name,
                    'inppl': num,
                    'maxppl' : room.maxppl,
                    'room_color':room.room_color,
                    'is_secret': room.is_secret
                })
            return Response({'my_room_list': my_room_list}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message' : "fail"}, status=status.HTTP_400_BAD_REQUEST)