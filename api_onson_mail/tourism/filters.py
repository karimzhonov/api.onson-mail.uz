import django_filters.rest_framework as filters
from django.db.models import Case, When, Q, Value
from .models import Region, Tour, Hotel, Country


class HotelFilter(filters.FilterSet):
    type = filters.BaseInFilter()
    region = filters.BaseInFilter()
    country = filters.BaseInFilter('region__country')

    class Meta:
        model = Hotel
        fields = ['type', 'region']


class CountryFilter(filters.FilterSet):

    class Meta:
        model = Country
        fields = ['can_from', 'can_to']


class RegionFilter(filters.FilterSet):
    country = filters.BaseInFilter()

    class Meta:
        model = Region
        fields = ['can_from', 'can_to', 'country']


class TourFilter(filters.FilterSet):
    type = filters.BaseInFilter('type')
    from_date = filters.DateFilter(method='filter_date')
    to_date = filters.DateFilter(method='filter_date')
    hotel = filters.BaseInFilter(method='filter_hotel')
    hotel_type = filters.BaseInFilter(method='filter_hotel_type')
    hotel_rating = filters.NumberFilter('day__hotel__stars')
    food = filters.BaseInFilter()
    from_country = filters.NumberFilter(method='filter_from_country')
    services = filters.BaseInFilter()
    region = filters.BaseInFilter('day__region')

    class Meta:
        model = Tour
        fields = [
            'type', 'from_country', 'to_country', 'from_date',
            'to_date', 'from_day', 'hot_tour', 'best_proposal',
            'food', 'hotel', 'hotel_type', 'hotel_rating', 'services'

        ]

    def filter_date(self, queryset, name, value):
        return queryset.filter(from_date__lte=value, to_date__gte=value)

    def filter_hotel(self, queryset, name, value):
        return queryset.filter(day__hotel_id__in=value)

    def filter_hotel_type(self, queryset, name, value):
        return queryset.filter(day__hotel__type_id__in=value)

    def filter_from_country(self, queryset, name, value):
        return queryset.annotate(
            _from_country_bool=Case(
                When(Q(with_flight=True), Value(True)),
                default=Q(from_country_id=value)
            )
        ).filter(_from_country_bool=True)
