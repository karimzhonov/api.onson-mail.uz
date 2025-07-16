import django_filters.rest_framework as filters
from .models import Hotel


class HotelFilter(filters.FilterSet):
    type = filters.BaseInFilter()
    region = filters.BaseInFilter()
    country = filters.BaseInFilter('region__country')
    food = filters.BaseInFilter('hotelfood__food')
    room = filters.BaseInFilter('hotelroom__room')
    service = filters.BaseInFilter('hotelservice__service')
    
    class Meta:
        model = Hotel
        fields = [
            'type', 'region', 'country',
            'food', 'room', 'service', 'stars'
        ]