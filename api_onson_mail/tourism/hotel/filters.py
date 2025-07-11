import django_filters.rest_framework as filters
from .models import Hotel


class HotelFilter(filters.FilterSet):
    type = filters.BaseInFilter()
    region = filters.BaseInFilter()
    country = filters.BaseInFilter('region__country')
    food = filters.BaseInFilter('hotelfood_set__food')
    room = filters.BaseInFilter('hotelroom_set__room')
    service = filters.BaseInFilter('hotelservice_set__service')
    
    class Meta:
        model = Hotel
        fields = [
            'type', 'region', 'country',
            'food', 'room', 'service'
        ]