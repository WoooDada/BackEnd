from django.shortcuts import render
from rest_framework import views


class studyroom(views.APIView):

   def get(self,request):


       return