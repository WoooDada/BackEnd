from django.http import HttpResponse
from rest_framework import views, status
from rest_framework.response import Response
from api.models import User
#from .serializers import
from .models import Daily_1m_content, Study_analysis


#전역변수로 버튼 초기화
start = False
stop = True

class study_button(views.APIView):

    def post(self, request):

        current_user_uid = request.data.get('uid')  # 요청한 사용자 받아오기
        user = User.objects.get(uid=current_user_uid)

        if user:
            try:
                if (request.data.get('start')=='true'):
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

    def get(self, request):

        Response()





class ten_min_data(views.APIView):

    def get(self,request):

        Response()

    def post(self, request):

        Response()