from webpush import send_user_notification


def send_notification(user, text, url):
    data = {
        "head": "Onson Mail",
        "body": text,
        "icon": "/logo.png",
        "tag": url
    }
    return send_user_notification(user=user, payload=data, ttl=1000)
