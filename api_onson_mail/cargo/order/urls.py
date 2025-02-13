from django.urls import path, include

from .views import OrderByNumberView

urlpatterns = [
    path('order/<number>/', OrderByNumberView.as_view()),
    path('admin/', include("cargo.order.api_admin.urls")),
]