from django.urls import path

from .views import CompanyView, CountryView

urlpatterns = [
    path('', CompanyView.as_view()),
    path('<slug>/country/', CountryView.as_view())
]