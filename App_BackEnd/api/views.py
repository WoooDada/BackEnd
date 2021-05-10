from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import signupSerializer,loginSerializer
from .models import User
from rest_framework import generics, status, views, request
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser


# 회원가입
class signup(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = signupSerializer

    def post(self, request):
        serializer = signupSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return JsonResponse({"message" : "uid duplicate"}, status=status.HTTP_400_BAD_REQUEST)


        if User.objects.filter(nickname=serializer.validated_data['nickname']).exists():
            return JsonResponse({"message" : "nickname duplicate"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(uid=serializer.validated_data['uid']).exists():
            return JsonResponse({"message": "uid duplicate"}, status=status.HTTP_400_BAD_REQUEST)
        else :
            serializer.is_active = False
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)




#로그인

class login(views.APIView):

    queryset = User.objects.all()
    serializer_class = loginSerializer
    def post(self, request):
        data = request.data
        serializer = loginSerializer(data=data)
        if not serializer.is_valid(raise_exception=False):
            #Response(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse({"message" : "error"}, status=status.HTTP_400_BAD_REQUEST)

        ser_uid = serializer['uid']
        #user = User.objects.get(uid=serializer.validated_data['uid'])
        user = User.objects.get(uid=serializer.validated_data['uid'])
        if user.password == serializer.validated_data['password'] :
        #if user.check_password(serializer['password']):

            return Response(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'check your id and password'}, status=status.HTTP_400_BAD_REQUEST)




"""
 def post(self, request):
        # if request.method == 'POST':
        req_data = request.data
        serializer = loginSerializer(data=req_data)

        try :
            serializer.is_valid(raise_exception=True)
        except:
            return JsonResponse({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

        # data = JSONParser().parse(request)
        # search_uid = data['uid']
        # obj = User.objects.get(uid = search_uid)
        obj = User.objects.filter(uid=serializer['uid'])
        # obj = User.objects.filter(uid=serializer.validated_data['uid'])

        if serializer['password'] == obj.password:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            JsonResponse({'message': 'wrong'}, status=status.HTTP_400_BAD_REQUEST)
"""



"""
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        search_uid = data['uid']
        obj = User.objects.get(uid=search_uid)

        if data['password'] == obj.password:
            return HttpResponse(status=200)
        else:
            return JsonResponse({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
"""





"""
        if serializer.validated_data['password'] == obj.password:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            JsonResponse({'message': 'wrong'}, status=status.HTTP_400_BAD_REQUEST)
"""

