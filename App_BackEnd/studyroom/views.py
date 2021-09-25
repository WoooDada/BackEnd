import jwt
from rest_framework import views, request, status
from rest_framework.response import Response
from api.models import User
from main.models import Room, Room_Enroll


def append_data(data, room):
    data.append({
                    "room_id":room.room_id,
                    "room_name": room.room_name,
                    "maxppl":room.maxppl,
                    "inppl":room.f_room.all().count(),
                    "room_comment":room.room_comment,
                    "is_secret":room.is_secret,
                    "room_tag":room.room_tag,
                    "room_color":room.room_color
                })
    return data


class studyroom(views.APIView):

    def post(self,request):

        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])

        roomname = request.data.get("room_name")
        if Room.objects.filter(room_name=roomname).exists() is True:
            return Response({"room_id": "-1"}, status=status.HTTP_200_OK)
        if request.data.get("is_secret") == 'T':
            is_secret = True
        else :
            is_secret = False
        try :

            if request.data.get("is_secret") == 'T' and request.data.get("room_pwd") == "" :
                return Response({"room_id": "-2"}, status=status.HTTP_200_OK)
            else :
                room = Room.objects.create(
                    maker_uid=user,
                    room_name=request.data.get("room_name"),
                    maxppl = request.data.get("maxppl"),
                    is_secret=is_secret,
                    room_pwd=request.data.get("room_pwd"),
                    room_tag=request.data.get("room_tag"),
                    room_comment=request.data.get("room_comment"),
                    room_color=request.data.get("room_color")
                )
                room.save()
                return Response({"room_id": room.room_id}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message":"fail"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            data=[]
            dict={}
            all=self.request.query_params.get('all')
            dict['all']=all
            college=self.request.query_params.get('college')
            dict['college']=college
            sat=self.request.query_params.get('sat')
            dict['sat']=sat
            gongmuwon=self.request.query_params.get('gongmuwon')
            dict['gongmuwon']=gongmuwon
            employment=self.request.query_params.get('employment')
            dict['employment']=employment
            certificate=self.request.query_params.get('certificate')
            dict['certificate']=certificate
            language=self.request.query_params.get('language')
            dict['language'] = language
            etc=self.request.query_params.get('etc')
            dict['etc']=etc
            university = self.request.query_params.get('university')
            dict['university'] = university
            sooneung = self.request.query_params.get('sooneung')
            dict['sooneung'] = sooneung

            keyword=self.request.query_params.get('keyword')



            for key,value in dict.items():
                if key=='all':
                    if value=='T':
                        room_query = Room.objects.all()
                        for room in room_query:
                            if keyword is not None :
                                if room.room_name.find(keyword) != -1:
                                    append_data(data,room)

                            else:
                                append_data(data,room)

                        break
                    else:
                        continue
                if value=='T':
                    room_query = Room.objects.filter(room_tag=key)
                    for room in room_query:
                        if keyword is not None:
                            if room.room_name.find(keyword) != -1:
                                append_data(data,room)
                        else:
                            append_data(data, room)

            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "fail"}, status=status.HTTP_400_BAD_REQUEST)
    """
    
    def put(self, request):

        try:
            get_room_id = request.data.get("room_id")
            access_token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            user = User.objects.get(uid=payload['id'])


            room_obj = Room_Enroll.objects.get(room_id=get_room_id, user_id=user)
            room_obj.current = False            #현재활동중 false로
            room_obj.save()

            return Response(status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "room delete fail"}, status=status.HTTP_400_BAD_REQUEST)

    """


class studyroom_pw(views.APIView):
    def post(self, request):
        access_token = request.headers.get('Authorization', None).split(' ')[1]
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        user = User.objects.get(uid=payload['id'])

        get_room_id = request.data.get("room_id")
        get_pw = request.data.get("password")

        real_pw = Room.objects.get(room_id=get_room_id).room_pwd

        if get_pw==real_pw:
            return Response({"correct": "T"}, status=status.HTTP_200_OK)
        else:
            return Response({"correct": "F"}, status=status.HTTP_200_OK)


class isfull(views.APIView):

    def get(self,request):
        try :
            room_id = self.request.query_params.get("room_id")
            count = Room_Enroll.objects.filter(room_id=room_id).count()
            maxppl = Room.objects.get(room_id=room_id).maxppl

            if count == maxppl:
                isfull = "T"
            else :
                isfull = "F"

            return Response({"isfull":isfull}, status=status.HTTP_200_OK)

        except Exception as e :
            print(e)
            return Response(status=status.HTTP_200_OK)