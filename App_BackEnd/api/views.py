from rest_framework.response import Response
from .serializers import signupSerializer,loginSerializer
from .models import User
from rest_framework import generics, status, views, request
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
import datetime, jwt
from django.utils import timezone

# 회원가입
class signup(views.APIView):

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
        else:
            serializer.is_active = False
            serializer.save()
           # user = serializer.create(serializer.validated_data)

           # user = User.objects.get(uid=serializer.validated_data['uid'])
            return Response(serializer.data, status=status.HTTP_200_OK)




#로그인

class login(views.APIView):

    queryset = User.objects.all()
    serializer_class = loginSerializer
    def post(self, request):
        data = request.data
        serializer = loginSerializer(data=data)
        user = User.objects.filter(uid=request.data['uid']).first()
        if not serializer.is_valid(raise_exception=False):
            #Response(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse({"message" : "check your id and password"}, status=status.HTTP_400_BAD_REQUEST)
        if user is None:
            return JsonResponse({"message": "check your id and password"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.password == serializer.validated_data['password']:
            return JsonResponse({"message": "check your id and password1"}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        date = now.date()  # 오늘 날짜

        payload = {
            'id': user.uid,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=9999),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token
        }
        return JsonResponse({'token': token}, status=status.HTTP_200_OK )











