from django.core.management import BaseCommand
from cargo.api_customs.egov import ApiPushService
from cargo.order.models import Order, _send_api_customs_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        api = ApiPushService()
        order = Order.objects.first()
        _send_api_customs_data([order.id], ['test_api-onson-mail-cargo'])

