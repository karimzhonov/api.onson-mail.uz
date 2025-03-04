from rest_framework import serializers

from .models import Day


class CalendarSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    def get_time(self, obj: Day):
        return obj.date_time.time().strftime("%H:%M")

    def get_end_time(self, obj: Day):
        return obj.end_date_time.time().strftime("%H:%M")

    class Meta:
        model = Day
        fields = '__all__'
