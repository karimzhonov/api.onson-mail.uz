from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TypeViewSet, RegionViewSet, ServiceViewSet, TourViewSet, FoodViewSet, CountryViewSet, HotelViewSet, HotelTypeViewSet

router = DefaultRouter()
router.register('type', TypeViewSet, 'tourism-type')
router.register('region', RegionViewSet, 'tourism-region')
router.register('tour', TourViewSet, 'tourism-tour')
router.register('food', FoodViewSet, 'tourism-food')
router.register('country', CountryViewSet, 'tourism-country')
router.register('hotel', HotelViewSet, 'tourism-hotel')
router.register('hotel-type', HotelTypeViewSet, 'tourism-hotel-type')
router.register('service', ServiceViewSet, 'tourism-service')

urlpatterns = [
    path('', include(router.urls))
]