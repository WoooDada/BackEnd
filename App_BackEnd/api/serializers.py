
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account
from rest_framework.exceptions import ValidationError


class signupSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', style={'input_type': 'password'})

    class Meta:
        model = Account
        fields = [
            'uid',
            'username',
            'password',
        ]

    def create(self, validated_data):

        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])
        user.save()

        account = Account.objects.create(user=user, **validated_data)
        account.username = user.username
        account.save()
        return account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            'id',
            'username',
        ]




class loginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password', style={'input_type': 'password'})
    account = AccountSerializer(allow_null=True, read_only=True)

    class Meta:
        model = User
        depth = 1
        fields = [
            'username',
            'password',
            'account',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        validation_data = dict(attrs)['user']
        username = validation_data.get('username', None)
        password = validation_data.get('password', None)

        try:
            user = User.objects.get(username=username)

        except:
            raise ValidationError("Incorrect Username/Password")

        if user.check_password(password):
            attrs['account'] = user.account
            return attrs
        raise ValidationError("Incorrect login/password.")
