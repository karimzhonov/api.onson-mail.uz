from django.urls import path

from .views import SaveWebPushInformationView

urlpatterns = [
    path('save_information/', SaveWebPushInformationView.as_view(), name='save_webpush_info'),
]
