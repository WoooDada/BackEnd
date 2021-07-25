from rest_framework import serializers
from .models import Monthly_tdl, Weekly_tdl, Daily_tdl

class monthly_serializer(serializers.ModelSerializer):

    class Meta:
        model = Monthly_tdl
        fields = '__all__'



class weekly_serializer(serializers.ModelSerializer):


    class Meta:
        model = Weekly_tdl
        fields = '__all__'



class daily_serializer(serializers.ModelSerializer):


    class Meta:
        model = Daily_tdl
        fields = '__all__'