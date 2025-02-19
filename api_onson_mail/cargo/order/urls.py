from django.urls import path, include

from .views import OrderByNumberView, StatusView

urlpatterns = [
    path('order/<number>/', OrderByNumberView.as_view()),
    path('status/', StatusView.as_view()),
    path('admin/', include("cargo.order.api_admin.urls")),
]