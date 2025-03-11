from webpush import send_user_notification
from .models import Notification


def send_notification(user, text, url):
    data = {
        "head": "Onson Mail",
        "body": text,
        "icon": "/logo.png",
        "tag": url
    }
    send_user_notification(user=user, payload=data, ttl=1000)
    return Notification.objects.create(user=user, data=data)
