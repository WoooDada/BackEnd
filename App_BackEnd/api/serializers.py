from .models import User
from rest_framework import serializers




#회원가입 serializer
class signupSerializer(serializers.ModelSerializer):

    uid = serializers.EmailField()
    nickname = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create(
            uid=validated_data['uid'],
            nickname=validated_data['nickname'],
            password=validated_data['password'],
        )
        user.set_password(validated_data['password'])
        # user.save()
        # user.is_active = False    #가입시 자동로그인 x
        return user


    class Meta:
        model = User
        fields = ['uid', 'nickname', 'password']


#로그인 serializer
class loginSerializer(serializers.ModelSerializer):

    uid = serializers.EmailField()
    password = serializers.CharField()


    class Meta:
        model = User
        fields = [
            'uid',
            'password',
        ]
        #extra_kwargs = {"password": {"write_only": True}}

"""
    def validate(self, attrs):

        uid = attrs['uid']
        password=attrs['password']

        try :
            user = User.objects.get(uid=uid)
        except:
            raise ValidationError("no Id")  # 계정 없음

        if user.check_password(password):
            return 1  # pw 불일치
        raise ValidationError("pw wrong")

"""



"""
   def validate(self, attrs):

        user = authenticate(
            uid=attrs['uid'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('invalid credentials provided')
        self.instance = user
        return user
"""