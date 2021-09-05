import asyncio
import json
import websockets
import base64
from channels.generic.websocket import WebsocketConsumer

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
        with open("d:\\workd2\\"+self.__filename, "wb") as handle:
        # 파일 작성
            handle.write(byte)
        # 콘솔 출력
        print("craete file - d:\\workd2\\"+self.__filename)




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




