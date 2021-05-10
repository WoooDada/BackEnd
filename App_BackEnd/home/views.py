from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
import pandas
from datetime import datetime

class badge_profile(views.APIView):

    def get(self,request):
        current_user = request.user  #요청한 사용자 받아오기
        user = User.objects.get(uid=current_user.uid)

        #user = User.objects.get(uid="woojung@love.com")   ##테스트데이터 line 13, 14 주석처리 후 진행

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
        #current_user = request.user
        #user = User.objects.get(uid=current_user.uid)
        user = User.objects.get(uid="woojung@love.com")

        if user:

            """
            
            start_date = request.query_params.get('from_date')
            end_date = request.query_params.get('to_date')

            https://newbiecs.tistory.com/272
            
            """
            graph =  [ {"date": "월", "concent_time": 5, "play_time": 5},
                {"date": "화", "concent_time": 1, "play_time": 0},
                {"date": "수", "concent_time": 1, "play_time": 2},
                {"date": "목", "concent_time": 5, "play_time": 5},
                {"date": "금", "concent_time": 3, "play_time": 2},
                {"date": "토", "concent_time": 2, "play_time": 2},
                {"date": "일", "concent_time": 4, "play_time": 2} ]

            return JsonResponse(graph, safe=False, status=status.HTTP_200_OK, json_dumps_params={'ensure_ascii': False},)
        else :
            return JsonResponse({"message": "no uid"}, status=status.HTTP_400_BAD_REQUEST)
