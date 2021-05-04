from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from account.api.serializers import signupSerializer


@api_view(['POST', ])
def signup_view(request):
    if request.method == 'POST':
        serializer = signupSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['username'] = account.username
        else:
            data = serializer.errors
        return Response(data)
        #return render(request, 'account/signup.html')

