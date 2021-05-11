from rest_framework import serializers

from api.models import User
from .models import Monthly_tdl, Weekly_tdl

class monthly_serializer(serializers.ModelSerializer):

    class Meta:
        model = Monthly_tdl
        fields = '__all__'

"""
    def create(self, validated_data):

        current_user_uid = validated_data['uid']

        monthly_tdl = Monthly_tdl.objects.create(

            m_todo_id= validated_data['m_todo_id'],
            uid = User.objects.get(uid=current_user_uid),
            stt_date = validated_data['stt_date'],
            end_date = validated_data['end_date'],
            m_content = validated_data['m_content'],
        )

        return monthly_tdl

"""


class weekly_serializer(serializers.ModelSerializer):


    class Meta:
        model = Weekly_tdl
        fields = '__all__'
