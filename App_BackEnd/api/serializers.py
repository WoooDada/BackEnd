from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import User
from rest_framework import serializers
from django.http import JsonResponse

#회원가입 serializer
class signupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            uid = validated_data['uid'],
            nickname = validated_data['nickname'],
            password = validated_data['password'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False    #가입시 자동로그인 x
        if User.objects.all().filter(uid=validated_data['uid']).exists():
            res = JsonResponse({'message': 'uid 중복'}, status=400)
            return res

        if User.objects.all().filter(nickname=validated_data['nickname']).exists():
            return JsonResponse({'message': 'nickname 중복'}, status=400)
        user.save()
        res = JsonResponse(status=200)
        print(res)
        return res

    class Meta:
        model = User
        fields = ['uid', 'nickname', 'password']



#로그인 serializer
class loginSerializer(serializers.ModelSerializer):

    uid = serializers.EmailField()
    #uid = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'uid',
            'password',
        ]
        extra_kwargs = {"password": {"write_only": True}}


    def validate(self, attrs):

        uid = attrs['uid']
        password=attrs['password']

        try :
            user = User.objects.get(uid=uid)
        except:
            return 0  # 계정 없음

        if user.check_password(password):
            return 1  # pw 불일치
        return 2



"""
   def validate(self, attrs):

        user = authenticate(
            uid=attrs['uid'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('invalid credentials provided')
        self.instance = user
        return user
"""