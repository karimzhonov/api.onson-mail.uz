from django.urls import path

from .views import SaveWebPushInformationView, NotificationView

urlpatterns = [
    path('', NotificationView.as_view()),
    path('save_information/', SaveWebPushInformationView.as_view(), name='save_webpush_info'),
]
