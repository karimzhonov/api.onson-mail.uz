from notification.client import send_notification
from cargo.models import CargoUser
from oauth.sms import send_sms
from oauth.telegram.notifications import send_message


ORDER_STATUS_TEXT = (
    ('create_time', 'Заказ #{number} создан и готовится к отправке.'),
    ('departure_datetime', 'Заказ #{number} проходит осмотр в аэропорту отправителя.'),
    ('enter_uzb_datetime', 'Заказ #{number} готовится к таможенному оформлению.'),
    ('process_customs_datetime', 'Заказ #{number} проходит таможенное оформление и вскоре будет направлен на доставку.'),
    ('process_local_datetime', 'Заказ #{number} находится в процессе доставки и скоро будет у вас.'),
    ('process_received_datetime', 'Заказ #{number} успешно доставлен.'),
)


def send_my_order_status(order):
    users = CargoUser.objects.filter(clients__in=[order.client])
    return [_send_my_order_status(user.user, order) for user in users]


def _send_my_order_status(user, order):
    text = dict(ORDER_STATUS_TEXT)[order.status].format(number=order.number)
    url = '/my/order?id={id}'.format(id=order.id)
    subject = f"Статус заказа {order.number}"
    send_notification(user, subject, text, url)
    
    message = f"{text}\n\nhttps://onson-mail.uz{url}"
    send_sms(user, message)

    message_html = f'{text} <a href="https://onson-mail.uz{url}">Посмотреть</a>'
    send_message(user, message_html)
