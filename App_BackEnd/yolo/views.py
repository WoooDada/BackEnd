from rest_framework import views, status
from rest_framework.response import Response
import json
import base64
from django.core.files.storage import default_storage
import cv2
import torch
from PIL import Image
from io import BytesIO

class testimage(views.APIView):
    def get(self,request):


        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')


        img = 'C:\BackEnd\App_BackEnd\yolo\\test\\aa.jpg'
        # Inference
        output = model(img)
        output.print()
        a = output.pandas().xyxy[0].to_json(orient="records")

        return Response({"message": a}, status=status.HTTP_200_OK)