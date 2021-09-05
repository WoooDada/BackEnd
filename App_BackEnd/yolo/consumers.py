import asyncio
import json
import base64
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from api.models import User

def base64_file(data, name=None):
    format, imgstr = data.split(';base64,')
    ext = format.split('/')[-1]

    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    file_name = "'myphoto." + ext
    User.image.save(file_name,data,save=True)




class sendConsumer(WebsocketConsumer):
    def connect(self):
      #  print("connected")
        self.accept()


    def disconnect(self, code):
      #  print("disconnected")
        pass


    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        base64_file(message, name='profile_picture')

        print("save success")


"""
class Node():

    # 생성자
    def __init__(self):
        # base64로 된 파일 데이터
        self.__data = ''


    # 파일 데이터 프로퍼티
    @property
    def data(self):
        return self.__data
    @data.setter
    def data(self, data):
        self.__data = data

    # 파일 데이터를 연속적으로 추가하는 함수
    def add_data(self, data):
        self.__data += data
    # 파일 전송이 끝났는지 확인하는 함수
    def is_complate(self):
    # 다운 받은 파일 크기와 요청된 파일 크기가 같으면 종료
        return self.__filesize == len(self.__data)
    # base64로 된 데이터를 파일로 저장하는 함수
    def save(self):
        # string을 byte로 변환(base64는 ascii코드로 구성되어 있음)
        byte = self.__data.encode("ASCII")
        # byte64를 binary로 디코딩
        byte = base64.b64decode(byte)
        # 파일 IO 오픈
       # with open("d:\\workd2\\"+self.__filename, "wb") as handle:
        with open("d:\\workd2\\wb") as handle:
        # 파일 작성
            handle.write(byte)
        # 콘솔 출력
     #   print("craete file - d:\\workd2\\"+self.__filename)
        print("craete file - d:\\workd2\\wb")



class sendConsumer(WebsocketConsumer):
    def connect(self):
      #  print("connected")
        self.accept()


    def disconnect(self, code):
      #  print("disconnected")
        pass


    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        print("receive success")

        node = Node()
        while True:
        # cmd를 받는다.
            cmd = await websocket.recv();
        # 처음 접속시 웹소켓에서 START 명령어가 온다.
        if cmd == 'START':
        # 파일 이름을 요청한다.
        await websocket.send("FILENAME");
        # 파일 이름에 대한 명령어가 오면,
        elif cmd == 'FILENAME':
        # 파일 이름을 받는다.
        node.filename = await websocket.recv();
        # 파일 사이즈를 요청한다.
        await websocket.send("FILESIZE");
        # 파일 사이즈에 대한 명령어가 오면
        elif cmd == 'FILESIZE':
        # 파일 사이즈를 설정한다.
        node.filesize = await websocket.recv();
        # 파일 데이터를 요청한다.
        await websocket.send("DATA");
        # 파일 데이터에 대한 명령어가 오면
        elif cmd == 'DATA':
        # 파일을 받아서 데이터를 추가한다.
        node.add_data(await websocket.recv());
        # 파일 전송이 끝나지 않으면
        if node.is_complate() == False:
        # 파일 데이터를 요청한다.
        await websocket.send("DATA");
        else:
        # 파일 전송이 끝나면 저장한다.
        node.save();
        # 웹 소켓을 닫는다.
        await websocket.close();
        # 종료!
        break;



"""
