from celery import shared_task
from contrib.sms import send_sms


@shared_task
def send_otp(phone: str, opt: str):
    return send_sms(phone, f"Ваш код подтверждения для onson-mail.uz: {opt}")
