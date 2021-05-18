from rest_framework import serializers
from .models import Daily_1m_content, Study_analysis

class daily_1m_serializer(serializers.ModelSerializer):

    class Meta:
        model = Daily_1m_content
        fields = '__all__'

    def create(self, validated_data):
        obj = Daily_1m_content.objects.create(**validated_data)

        return obj.save()


class study_ana_serializer(serializers.ModelSerializer):

    class Meta:
        model = Study_analysis
        fields = '__all__'
