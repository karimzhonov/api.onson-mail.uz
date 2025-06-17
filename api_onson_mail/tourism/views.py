from django.db.models import OuterRef, Subquery
from rest_framework.viewsets import ReadOnlyModelViewSet
from .filters import RegionFilter, TourFilter, CountryFilter, HotelFilter
from .models import Type, Region, Tour, Price, Food, Hotel, HotelType, Country, Service
from .serializers import TypeSerializer, RegionSerializer, ServiceSerializer, TourSerializer, TourListSerializer, CountrySerializer, HotelTypeSerializer, HotelSerializer, FoodSerializer


class HotelTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = HotelTypeSerializer
    queryset = HotelType.objects.all()


class HotelViewSet(ReadOnlyModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    filterset_class = HotelFilter


class FoodViewSet(ReadOnlyModelViewSet):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()


class TypeViewSet(ReadOnlyModelViewSet):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()


class ServiceViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class CountryViewSet(ReadOnlyModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.filter(active=True)
    filterset_class = CountryFilter


class RegionViewSet(ReadOnlyModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.filter(active=True)
    filterset_class = RegionFilter


class TourViewSet(ReadOnlyModelViewSet):
    filterset_class = TourFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return TourListSerializer
        return TourSerializer

    def get_queryset(self):
        return Tour.objects.annotate(
            min_price_b2b=Subquery(
                Price.objects.filter(tour_id=OuterRef('id')).order_by('price_b2b').values('price_b2b')[:1]
            ),
            min_price_b2c=Subquery(
                Price.objects.filter(tour_id=OuterRef('id')).order_by('price_b2b').values('price_b2c')[:1]
            ),
        ).prefetch_related('day_set', 'type', 'price_set', 'image_set')
