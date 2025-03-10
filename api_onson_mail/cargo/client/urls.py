from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .myid import myid_auth, myid_code
from .views import ClientViewSet

router = DefaultRouter()
router.register('client', ClientViewSet, '')

urlpatterns = [
    path("myid/auth/", myid_auth),
    path("myid/code/<code>/", myid_code),
    path('admin/', include("cargo.client.api_admin.urls")),
]
