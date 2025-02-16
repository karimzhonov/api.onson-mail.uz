from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('order', views.OrderViewSet, 'admin-order')
router.register('part', views.PartViewSet, 'admin-part')

urlpatterns = [
    path('', include(router.urls)),
    path('products-generator/<price>/', views.ProductGeneratorView.as_view()),
]