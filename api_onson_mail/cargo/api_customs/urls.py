from django.urls import path
from .views import MQView

urlpatterns = [
    path('mq/', MQView.as_view()),
]