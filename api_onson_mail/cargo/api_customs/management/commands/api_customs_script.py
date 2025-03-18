from django.core.management import BaseCommand
from cargo.api_customs.tasks import request_subscribers

class Command(BaseCommand):
    def handle(self, *args, **options):
        request_subscribers()
