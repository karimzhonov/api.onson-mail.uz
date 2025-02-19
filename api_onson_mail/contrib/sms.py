import json
import os
import requests


def send_sms(phone: str, text: str):
    phone = phone.replace('+', '')
    url = os.getenv('SMS_URL')
    data = {
        'login': os.getenv('SMS_LOGIN'),
        'password': os.getenv('SMS_PASSWORD'),
        'data': json.dumps([
            {"phone": phone, "text": text}
        ], ensure_ascii=False, indent=2)
    }
    return requests.post(url, json=data).json(encoding='utf-8')


def send_list_sms(data: list[dict[str: str]]):
    for d in data:
        d['phone'] = d['phone'].replace('+', '')
    url = os.getenv('SMS_URL')
    data = {
        'login': os.getenv('SMS_LOGIN'),
        'password': os.getenv('SMS_PASSWORD'),
        'data': json.dumps(data, ensure_ascii=False, indent=2)
    }
    return requests.post(url, json=data).json()
