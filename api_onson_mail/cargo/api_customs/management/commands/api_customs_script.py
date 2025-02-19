from django.core.management import BaseCommand
from cargo.api_customs.egov import ApiPushService


class Command(BaseCommand):
    def handle(self, *args, **options):
        api = ApiPushService()
        print(api.get_statistics())

