from notification.client import send_notification
from cargo.models import CargoUser


ORDER_STATUS_TEXT = (
    ('create_time', 'Cоздан'),
    ('departure_datetime', 'Отправлено'),
    ('enter_uzb_datetime', 'Узбекистане'),
    ('process_customs_datetime', 'В Таможне'),
    ('process_local_datetime', 'В доставке'),
    ('process_received_datetime', 'Доставлен'),
)


def send_my_order_status(order):
    users = CargoUser.objects.filter(clients__in=[order.client])
    text = dict(ORDER_STATUS_TEXT)[order.status].format(number=order.number)
    return [send_notification(user.user, text, '/my/order?id={id}'.format(id=order.id)) for user in users]
