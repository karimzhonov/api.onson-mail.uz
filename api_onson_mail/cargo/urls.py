from django.urls import include, path

urlpatterns = [
    path('order/', include('cargo.order.urls')),
    path('api_customs/', include('cargo.api_customs.urls')),
]