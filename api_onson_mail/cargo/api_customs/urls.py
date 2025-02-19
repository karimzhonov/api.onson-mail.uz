from django.urls import path
from .views import MQView, MQTestView, MQTestReceiveView

urlpatterns = [
    path('mq/', MQView.as_view()),
    path('mq/test/health-check', MQTestView.as_view()),
    path('mq/test/receive', MQTestReceiveView.as_view()),
]