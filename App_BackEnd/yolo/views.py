from rest_framework import views, status
from rest_framework.response import Response
import json
import base64
from django.core.files.storage import default_storage
import cv2
import torch
from PIL import Image
from io import BytesIO


def copy_attr(a, b, include=(), exclude=()):
    # Copy attributes from b to a, options to only include [...] and to exclude [...]
    for k, v in b.__dict__.items():
        if (len(include) and k not in include) or k.startswith('_') or k in exclude:
            continue
        else:
            setattr(a, k, v)


class testimage(views.APIView):
    def get(self,request):

       # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='static/21_08_30_best.pt')

        model = model.fuse().autoshape()

        img = 'static/aa.jpg'

        output = model(img)
        output.print()
        a = output.pandas().xyxy[0].to_json(orient="records")
        return Response({"message": a}, status=status.HTTP_200_OK)
    """

        checkpoint_ = torch.load('21_08_30_best.pt')['model']
        model.load_state_dict(checkpoint_.state_dict())

        copy_attr(model, checkpoint_, include=('yaml', 'nc', 'hyp', 'names', 'stride'), exclude=())

        model = model.fuse().autoshape()

        img = 'C:\BackEnd\App_BackEnd\yolo\\test\\aa.jpg'
        # Inference
        output = model(img)
        output.print()
        a = output.pandas().xyxy[0].to_json(orient="records")
        """
