from webpush import send_user_notification
from .models import Notification


def send_notification(user, text, url):
    data = {
        "head": "Onson Mail",
        "body": text,
        "icon": "/logo.png",
    }
    n = Notification.objects.create(user=user, data=data, url=url)
    data['tag'] = n.id
    send_user_notification(user=user, payload=data, ttl=1000)
    return 
