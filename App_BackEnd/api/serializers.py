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
            password = validated_data['password']
        )
        if User.objects.all().filter(uid=validated_data['uid']).exists():
            return JsonResponse({'message': 'uid 중복'}, status=400)
        if User.objects.all().filter(nickname=validated_data['nickname']).exists():
            return JsonResponse({'message': 'nickname 중복'}, status=400)
        user.save()
        return JsonResponse(status=200)

    class Meta:
        model = User
        fields = ['uid', 'nickname', 'password']



#로그인 serializer
class loginSerializer(serializers.ModelSerializer):

    uid = serializers.CharField(source='user.uid')
    password = serializers.CharField(source='user.password')


    class Meta:
        model = User
        depth = 1
        fields = [
            'uid',
            'password',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        validation_data = dict(attrs)['user']
        uid = validation_data.get('uid', None)
        password = validation_data.get('password', None)
        try:
            user = User.objects.get(uid=uid)

        except:
            raise ValidationError("Incorrect Username/Password")

        if user.check_password(password):
            attrs['account'] = user.account
            return attrs
        raise ValidationError("Incorrect login/password.")