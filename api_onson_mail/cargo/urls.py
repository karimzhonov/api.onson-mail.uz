from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MeView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('order/', include('cargo.order.urls')),
    path('api_customs/', include('cargo.api_customs.urls')),
    path('client/', include('cargo.client.urls')),
    path('me/', MeView.as_view()),
]