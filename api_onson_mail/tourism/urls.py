from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TypeViewSet, RegionViewSet, ServiceViewSet, TourViewSet, FoodViewSet, CountryViewSet

router = DefaultRouter()
router.register('type', TypeViewSet, 'tourism-type')
router.register('region', RegionViewSet, 'tourism-region')
router.register('tour', TourViewSet, 'tourism-tour')
router.register('food', FoodViewSet, 'tourism-food')
router.register('country', CountryViewSet, 'tourism-country')
router.register('service', ServiceViewSet, 'tourism-service')

urlpatterns = [
    path('', include(router.urls))
]