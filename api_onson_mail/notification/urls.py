from django.urls import path

from .views import SaveWebPushInformationView, NotificationView, NotificationReadView

urlpatterns = [
    path('', NotificationView.as_view()),
    path('<int:id>/read/', NotificationReadView.as_view()),
    path('save_information/', SaveWebPushInformationView.as_view(), name='save_webpush_info'),
]
