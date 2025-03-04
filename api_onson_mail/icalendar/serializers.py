from rest_framework import serializers

from .models import Day


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'
