from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, StatusView, OrderByNumberView

router = DefaultRouter()
router.register('order', OrderViewSet, '')

urlpatterns = [
    path('', include(router.urls)),
    path('number/<number>/', OrderByNumberView.as_view()),
    path('status/', StatusView.as_view()),
    path('admin/', include("cargo.order.api_admin.urls")),
]