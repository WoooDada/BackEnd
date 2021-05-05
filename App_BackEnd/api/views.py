from django.contrib.auth import authenticate
from requests import Response

from .serializers import signupSerializer,loginSerializer
from .models import User
from rest_framework import generics, status, views, request
from django.http import JsonResponse, response, HttpResponse


# 회원가입
class signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = signupSerializer


#로그인

class login(views.APIView):

    queryset = User.objects.all()
    serializer_class = loginSerializer

    def post(self, request):
        data = request.data
        serializer = loginSerializer(data=data)

        if serializer == 2:
            return JsonResponse(status=200)
        elif serializer == 1:
            return JsonResponse({'message': 'wrong'}, status=400)
        return JsonResponse({'message': 'no'}, status=400)
