import os
import hmac
import hashlib
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed


def validate(auth_data):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    check_hash = auth_data['hash']
    del auth_data['hash']
    
    data_check_arr = []
    for key, value in auth_data.items():
        data_check_arr.append(f"{key}={value}")
    
    data_check_arr.sort()
    data_check_string = "\n".join(data_check_arr)

    
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hash_value = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    
    if hash_value != check_hash:
        raise AuthenticationFailed(
            _("Given token not valid for any token type"),
            code='bot_token'
        )

    if (timezone.now().timestamp() - auth_data['auth_date']) > 86400:
        raise AuthenticationFailed(
            _("Given token not valid for any token type"),
            code='bot_token'
        )
    
    return auth_data 


def validate_webapp_auth(init_data: dict):
    """
    Проверка Telegram WebApp initData.
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    check_hash = init_data.get("hash")
    if not check_hash:
        raise AuthenticationFailed(_("Missing hash"), code="bot_token")

    # собираем data-check-string
    data_check_arr = []
    for key, value in init_data.items():
        if key == "hash":
            continue
        if isinstance(value, dict):
            # user / chat приходят как JSON → сериализуем
            value = str(value)
        data_check_arr.append(f"{key}={value}")

    data_check_arr.sort()
    data_check_string = "\n".join(data_check_arr)

    # считаем HMAC-SHA256
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hash_value = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if hash_value != check_hash:
        raise AuthenticationFailed(
            _("Given token not valid for any token type"),
            code="bot_token",
        )

    # проверяем время (auth_date обязательно есть)
    try:
        auth_date = int(init_data["auth_date"])
    except (KeyError, ValueError):
        raise AuthenticationFailed(_("Invalid auth_date"), code="bot_token")

    if (timezone.now().timestamp() - auth_date) > 86400:
        raise AuthenticationFailed(
            _("Auth date expired"),
            code="bot_token",
        )

    return init_data