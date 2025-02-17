from django.urls import path, include
from .myid import myid_auth, myid_code

urlpatterns = [
    path("myid/auth/", myid_auth),
    path("myid/code/<code>/", myid_code),
    path('admin/', include("cargo.client.api_admin.urls")),
]
