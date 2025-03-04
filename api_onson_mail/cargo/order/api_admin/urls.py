from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('order', views.OrderViewSet, 'admin-order')
router.register('part', views.PartViewSet, 'admin-part')
router.register('product', views.ProductViewSet, '')
urlpatterns = [
    path('<company_sub>/', include(router.urls)),
]