from django.contrib.auth import authenticate
from rest_framework.response import Response
from .serializers import signupSerializer,loginSerializer
from .models import User
from rest_framework import generics, status, views, request
from django.http import JsonResponse, HttpResponse


# 회원가입
class signup(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = signupSerializer

    def post(self, request, *args, **kwargs):
        serializer = signupSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return JsonResponse({"message" : "error"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(uid=serializer.validated_data['uid']).first() is None:
            serializer.save()
            #print(Response(serializer.data))
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif User.objects.filter(uid=serializer.validated_data['uid']).exists():
            return JsonResponse({"message" : "duplicate email"}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(nickname=serializer.validated_data['nickname']).exists():
            return JsonResponse({"message" : "duplicate nickname"}, status=status.HTTP_400_BAD_REQUEST)




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
