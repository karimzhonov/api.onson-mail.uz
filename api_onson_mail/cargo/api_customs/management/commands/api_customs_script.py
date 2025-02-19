from django.core.management import BaseCommand
from cargo.api_customs.egov import ApiPushService
from cargo.api_customs.models import System


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.request_subscribers()

    @staticmethod
    def request_subscribers():
        api = ApiPushService()
        data = api.get_subscribers()
        for d in data:
            system, _ =System.objects.update_or_create({
                "company_name": d.get("companyName"),
                "system_name": d.get("systemName"),
                "description": d.get("description"),
                "status": d.get("status"),
            }, system_name=d.get("systemName"))
            print(system)
