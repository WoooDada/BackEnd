import datetime
import jwt
from django.http import JsonResponse
from rest_framework import views, status
from api.models import User


class myprofile(views.APIView):

    def get(self, request):
        try :
            access_token = request.headers.get('Authorization', None)
            access_token = access_token.split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            uid = payload['id']        #uid자체

            categ_array = ['college', 'sat', 'gongmuwon', 'employment', 'certificate', 'language', 'etc']
            categ_bool_array=['F','F','F','F','F','F','F']

            user = User.objects.get(uid=uid)
            like_category = user.like_category
            birth = user.birth
            sex = user.sex
            if sex is None:
                sex = 'U'
            if birth is None:
                birth = datetime.datetime.now().date()
            if like_category is not None and like_category != '':
                like_category = like_category.split("-")
                for like in like_category:
                    like_index = categ_array.index(like)
                    categ_bool_array[like_index]='T'


            send_data = {
                "nickname": user.nickname,
                "sex": sex,
                "birth": birth,
                "like_category": {
                    "college": categ_bool_array[0],
                    "sat":categ_bool_array[1],
                    "gongmuwon" :categ_bool_array[2] ,
                    "employment" :categ_bool_array[3] ,
                    "certificate" :categ_bool_array[4] ,
                    "language" : categ_bool_array[5],
                    "etc":categ_bool_array[6]
                }
            }

            return JsonResponse({'send_data':send_data}, status=status.HTTP_200_OK )

        except Exception as e :
            print(e)
            return JsonResponse({'message': 'fail'}, status=400)



    def put(self,request):
        try :
            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])

            user.nickname = request.data.get('nickname')
            user.sex = request.data.get('sex')
            user.birth = request.data.get('birth')
            like_categ = request.data.get('like_category')
            str = ''
            for key,value in like_categ.items() :
                if value == 'T':
                    if key == 'etc ':
                        str += key
                    else :
                        str += key + "-"

            user.like_category = str
            user.save()

            return JsonResponse({'message':'success'}, status=status.HTTP_200_OK )

        except Exception as e:
            print(e)
            return JsonResponse({'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)