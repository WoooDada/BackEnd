from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def main(request):
    return render(request, 'mainpage/main.html')