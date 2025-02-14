import os
import requests


def send_sms(phone: str, text: str):
    phone = phone.replace('+', '')
    url = os.getenv('SMS_URL')
    data = {
        'login': os.getenv('SMS_LOGIN'),
        'password': os.getenv('SMS_PASSWORD'),
        'data': [
            {"phone": phone, "text": text}
        ]
    }
    return requests.post(url, json=data).json()


def send_list_sms(data: list[dict[str: str]]):
    for d in data:
        d['phone'] = d['phone'].replace('+', '')
    url = os.getenv('SMS_URL')
    data = {
        'login': os.getenv('SMS_LOGIN'),
        'password': os.getenv('SMS_PASSWORD'),
        'data': data
    }
    return requests.post(url, json=data).json()