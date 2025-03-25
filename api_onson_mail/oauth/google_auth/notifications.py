from django.core.mail import send_mail
from django.conf import settings


def send_email(user, subject, text):
    try:
        if hasattr(user, 'googleuser'):
            send_mail(subject, text, settings.EMAIL_HOST_USER, [user.googleuser.email])
    except Exception as _exp:
        print("GMail", _exp)
