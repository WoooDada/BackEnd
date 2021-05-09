from rest_framework import serializers

from .models import Daily_1m_concent

class daily_concent_serializer(serializers.ModelSerializer):
    class Meta:
        model = Daily_1m_concent
        fields='__all__'
