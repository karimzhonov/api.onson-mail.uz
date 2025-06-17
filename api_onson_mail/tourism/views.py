from django.db.models import OuterRef, Subquery
from rest_framework.viewsets import ReadOnlyModelViewSet
from .filters import RegionFilter, TourFilter, CountryFilter, HotelFilter
from .models import Type, Region, Tour, Price, Food, Hotel, HotelType, Country, Service
from .serializers import TypeSerializer, RegionSerializer, ServiceSerializer, TourSerializer, TourListSerializer, CountrySerializer, HotelTypeSerializer, HotelSerializer, FoodSerializer


class HotelTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = HotelTypeSerializer
    queryset = HotelType.objects.all()
    authentication_classes = ()
    permission_classes = ()


class HotelViewSet(ReadOnlyModelViewSet):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    filterset_class = HotelFilter
    authentication_classes = ()
    permission_classes = ()


class FoodViewSet(ReadOnlyModelViewSet):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    authentication_classes = ()
    permission_classes = ()


class TypeViewSet(ReadOnlyModelViewSet):
    serializer_class = TypeSerializer
    queryset = Type.objects.all()
    authentication_classes = ()
    permission_classes = ()


class ServiceViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    authentication_classes = ()
    permission_classes = ()


class CountryViewSet(ReadOnlyModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.filter(active=True)
    filterset_class = CountryFilter
    authentication_classes = ()
    permission_classes = ()


class RegionViewSet(ReadOnlyModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.filter(active=True)
    filterset_class = RegionFilter
    authentication_classes = ()
    permission_classes = ()


class TourViewSet(ReadOnlyModelViewSet):
    filterset_class = TourFilter
    authentication_classes = ()
    permission_classes = ()

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
