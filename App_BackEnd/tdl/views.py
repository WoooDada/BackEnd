from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
# Create your views here.


class monthly_tdl(views.APIView):

    def get(self, request):

        return Response()



class weekly_tdl(views.APIView):

    def get(self, request):
        return Response()




class daily_tdl(views.APIView):

    def get(self, request):
        return Response()