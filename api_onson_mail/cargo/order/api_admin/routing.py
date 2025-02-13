from django.urls import path

from .consumers import QrCodeSessionConsumer


websocket_urlpatterns = [
    path('api/ws/cargo/order/admin/qrcode-session/', QrCodeSessionConsumer.as_asgi()),
]