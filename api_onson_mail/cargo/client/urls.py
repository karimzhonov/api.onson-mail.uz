from django.urls import path

from .myid import myid_auth, myid_code

urlpatterns = [
    path("myid/auth/", myid_auth),
    path("myid/code/<code>/", myid_code)
]
