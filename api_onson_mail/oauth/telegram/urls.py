from django.urls import path
from .views import TelegramAuthView, TelegramWebAppAuthView


urlpatterns = [
    path('', TelegramAuthView.as_view()),
    path('webapp/', TelegramWebAppAuthView.as_view())  
]
