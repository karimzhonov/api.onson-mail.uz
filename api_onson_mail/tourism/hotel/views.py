from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import HotelSerializer, HotelTypeSerializer, HotelRoomTypeSerializer, HotelServiceTypeSerializer
from .models import HotelType, Hotel, HotelRoomType, HotelServiceType
from .filters import HotelFilter


class HotelTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = HotelTypeSerializer
    queryset = HotelType.objects.all()
    authentication_classes = ()
    permission_classes = ()


class HotelRoomTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = HotelRoomTypeSerializer
    queryset = HotelRoomType.objects.all()
    authentication_classes = ()
    permission_classes = ()


class HotelServiceTypeViewSet(ReadOnlyModelViewSet):
    serializer_class = HotelServiceTypeSerializer
    queryset = HotelServiceType.objects.all()
    authentication_classes = ()
    permission_classes = ()


class HotelViewSet(ReadOnlyModelViewSet):
    serializer_class = HotelSerializer
    filterset_class = HotelFilter
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        return Hotel.objects.all().select_related(
            'type', 'region'
        ).prefetch_related(
            'hotelfood_set', 'hotelroom_set', 'hotelservice_set', 'hotelimage_set',
            'hotelfood_set__food', 'hotelroom_set__room', 'hotelservice_set__service',
        )
