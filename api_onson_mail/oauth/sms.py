from celery import shared_task
from contrib.sms import send_sms as _send_sms


@shared_task
def send_otp(phone: str, opt: str):
    return _send_sms(phone, f"Ваш код подтверждения для onson-mail.uz: {opt}")


def send_sms(user, message):
    try:
        if user.phone:
            _send_sms(user.phone, message)
    except Exception as _exp:
        print("SMS", _exp)
