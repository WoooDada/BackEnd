
from .serializers import signupSerializer,loginSerializer
from .models import User
from rest_framework import generics, status, views
from django.http import JsonResponse, response


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
        serializer = signupSerializer(data=data)
        try:
            if serializer.is_valid(raise_exception=True):
                new_date = serializer.data
                return JsonResponse(status=200)
        except:
            return JsonResponse({'message': 'wrong'}, status=400)

