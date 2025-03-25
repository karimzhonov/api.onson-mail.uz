import os
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_message(user, message):
    try:
        if hasattr(user, "telegramuser"):
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            data = {"chat_id": user.telegramuser.id, "text": message, "parse_mode": "HTML"}
            requests.post(url, data=data)
    except Exception as _exp:
        print("Telegram", _exp)
