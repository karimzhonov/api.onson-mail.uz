from celery import shared_task
from cargo.api_customs.egov import ApiPushService
from cargo.api_customs.models import System
from company.models import Company


@shared_task
def request_subscribers():
    for company in Company.objects.all():
        api = ApiPushService(company.sub, company.private_key)
        data = api.get_subscribers()
        for d in data:
            system, _ =System.objects.update_or_create({
                "company_name": d.get("companyName"),
                "system_name": d.get("systemName"),
                "description": d.get("description"),
                "status": d.get("status"),
                "company": company
            }, system_name=d.get("systemName"))
            print(system, company)
