from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelTypeViewSet, HotelViewSet, HotelRoomTypeViewSet, HotelServiceTypeViewSet

router = DefaultRouter()

router.register('hotel', HotelViewSet, 'tourism-hotel')
router.register('hotel-type', HotelTypeViewSet, 'tourism-hotel-type')
router.register('hotel-room', HotelRoomTypeViewSet, 'hotel-room-type')
router.register('hotel-service', HotelServiceTypeViewSet, 'hotel-service-type')

urlpatterns = [
    path('', include(router.urls))
]
