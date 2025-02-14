import uuid
from celery import shared_task
from django.db import models
from django.utils import timezone
from cargo.api_customs.egov import ApiPushService
from cargo.api_customs.models import System
from .api_admin.consumers import send_data_to_session

STATUSES = (
    ('departure_datetime', 'Yolga chiqdi'),
    ('enter_uzb_datetime', 'UZBga keldi'),
    ('process_customs_datetime', 'Tamojnada'),
    ('process_local_datetime', 'Dastavkada'),
    ('process_received_datetime', 'Yetkasib berildi'),
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
        systems = list(System.objects.filter(active=True).values_list("system_name", flat=True))
        _send_request.delay(part_number=self.number, systems=list(systems))


@shared_task(task_name='egov_receive')
def _send_request(part_number, systems):
    api = ApiPushService()
    success_data = []
    for order in Order.objects.select_related("parts", "parts__country", "client").filter(parts_id=part_number):
        json = order.serialized_data
        response = api.create_or_update(order.id, json, systems)
        success_data.append({"id": str(order.id), "response": response.text, "status": response.status_code})
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
    facture_price = models.FloatField(null=True)


    @property
    def status(self):
        if self.process_received_datetime:
            return 'process_received_datetime'
        elif self.process_local_datetime:
            return 'process_local_datetime'
        elif self.process_customs_datetime:
            return 'process_customs_datetime'
        elif self.enter_uzb_datetime:
            return 'enter_uzb_datetime'
        return 'departure_datetime'

    @property
    def delivery_price(self):
        return self.parts.country.price_per * self.weight

    @property
    def serialized_data(self):
        return {
            "shipmentId": str(self.id),
            "shipmentNumber": str(self.number),
            "shipmentIdCreatTime": self.create_time.timestamp(),
            "shipmentOrgName": str(self.parts.country.org_name),
            "shipmentOrgStir": str(self.parts.country.org_stir),
            "shipmentCountryCode": str(self.parts.country.code),
            "shipmentCountry": str(self.parts.country.name),
            "shipmentSendOrg": None,
            "shipmentDepartureTime": self.departure_datetime.timestamp(),
            "shipmentEnterUzb": self.enter_uzb_datetime.timestamp(),
            "shipmentProcessCustoms": self.process_customs_datetime.timestamp(),
            "shipmentProcessLocal": self.process_local_datetime.timestamp(),
            "shipmentReceivedInd": self.process_received_datetime.timestamp(),
        }

    def send_ws_data(self, user_id):
        from .api_admin.serializers import OrderSerializer

        send_data_to_session(user_id, OrderSerializer(self).data)
