from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CalendarSerializer
from .models import Day


class CalendarView(ListAPIView):
    serializer_class = CalendarSerializer
    permission_classes = ()
    authentication_classes = ()
    pagination_class = None

    def get_queryset(self):
        return Day.objects.filter(date_time__date=timezone.now().date())
