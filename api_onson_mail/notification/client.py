from webpush import send_user_notification
from .models import Notification


def send_notification(user, subject, text, url):
    try:
        data = {
            "head": subject,
            "body": text,
            "icon": "/logo.png",
        }
        n = Notification.objects.create(user=user, data=data, url=url)
        data['tag'] = n.id
        send_user_notification(user=user, payload=data, ttl=1000)
    except Exception as _exp:
        print("WebPush", _exp)
