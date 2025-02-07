import uuid
from celery import shared_task
from django.db import models
from django.utils import timezone
from cargo.api import request as api_request


STATUSES = (
    ('departure_datetime', 'Yolga chiqdi'),
    ('enter_uzb_datetime', 'UZBga keldi'),
    ('process_customs_datetime', 'Tamojnada'),
    ('process_local_datetime', 'Dastavkada'),
    ('received_datetime', 'Yetkasib berildi'),
)


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    org_name = models.CharField(max_length=100)
    org_stir = models.CharField(max_length=100)
    send_org = models.CharField(max_length=100, blank=True, null=True)
    price_per = models.FloatField()

    def __str__(self):
        return self.name


class Part(models.Model):
    number = models.IntegerField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.CharField("Статус", max_length=50, default=STATUSES[0][0], choices=STATUSES)

    def __str__(self):
        return f"{self.number} - {self.country}"

    def send_request(self):
        Order.objects.filter(parts=self).update(**{self.status: timezone.now()})
        _send_request.delay(self.number)


@shared_task
def _send_request(part_number):
    success_data = []
    for order in Order.objects.select_related("parts", "parts__country", "client").filter(parts_id=part_number):
        json = order.serialized_data
        response = api_request(order.id, json)
        success_data.append({"body": json, "response": response.text, "status": response.status_code})
    return success_data


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=100, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    departure_datetime = models.DateTimeField(blank=True, null=True)
    enter_uzb_datetime = models.DateTimeField(blank=True, null=True)
    process_customs_datetime = models.DateTimeField(blank=True, null=True)
    process_local_datetime = models.DateTimeField(blank=True, null=True)
    process_received_datetime = models.DateTimeField(blank=True, null=True)

    parts = models.ForeignKey(Part, on_delete=models.CASCADE)
    client = models.ForeignKey("client.Client", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    weight = models.FloatField()

    @property
    def delivery_price(self):
        return self.parts.country.price_per * self.weight

    @property
    def serialized_data(self):
        return {
            "shipmentId": str(self.id),
            "shipmentNumber": str(self.number),
            "shipmentIdCreatTime": str(self.create_time),
            "shipmentOrgName": str(self.parts.country.org_name),
            "shipmentOrgStir": str(self.parts.country.org_stir),
            "shipmentCountryCode": str(self.parts.country.code),
            "shipmentCountry": str(self.parts.country.name),
            "shipmentSendOrg": None,
            "shipmentDepartureTime": str(self.departure_datetime),
            "shipmentEnterUzb": str(self.enter_uzb_datetime),
            "shipmentProcessCustoms": str(self.process_customs_datetime),
            "shipmentProcessLocal": str(self.process_local_datetime),
            "shipmentReceivedInd": str(self.process_received_datetime),
        }
