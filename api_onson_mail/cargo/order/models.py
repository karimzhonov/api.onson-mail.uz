import uuid
import string
from celery import shared_task
from django.contrib.gis.db import models
from django.utils import timezone
from cargo.api_customs.egov import ApiPushService
from cargo.api_customs.models import System
from .api_admin.consumers import send_data_to_session

STATUSES = (
    ('create_time', 'Cоздан'),
    ('departure_datetime', 'Отправлено'),
    ('enter_uzb_datetime', 'Узбекистане'),
    ('process_customs_datetime', 'В Таможне'),
    ('process_local_datetime', 'В доставке'),
    ('process_received_datetime', 'Доставлен'),
)


class Part(models.Model):
    number = models.IntegerField(primary_key=True)
    country = models.ForeignKey("company.Country", on_delete=models.CASCADE)
    status = models.CharField("Статус", max_length=50, default=STATUSES[0][0], choices=STATUSES)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-number']

    def __str__(self):
        return f"{self.number} - {self.country}"

    def send_api_customs_data(self):
        orders = Order.objects.filter(parts=self)
        orders.update(**{self.status: timezone.now()})

        for order in Order.objects.filter(parts=self):
            order.send_api_customs_data()


def _number_to_string(n):
    alphabet = string.ascii_uppercase
    base = len(alphabet)
    result = []
    n -= 1  # Коррекция для 1-индексации

    while n >= 0:
        result.append(alphabet[n % base])
        n = n // base - 1

    s = ''.join(reversed(result))
    return (3 - len(s)) * "A" + s

def _generate_order_number(order):
    count = Order.objects.count() + 1
    number = str(count % 100000)
    seria = count // 100000
    s = _number_to_string(seria + 1)
    n = (5 - len(number)) * "0" + number
    part = str(order.parts.number)
    p = (3 - len(part)) * "0" + part
    return f"{s}{n}P{p}"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=100, unique=True, editable=False)
    create_time = models.DateTimeField(auto_now_add=True)
    departure_datetime = models.DateTimeField(blank=True, null=True)
    enter_uzb_datetime = models.DateTimeField(blank=True, null=True)
    process_customs_datetime = models.DateTimeField(blank=True, null=True)
    process_local_datetime = models.DateTimeField(blank=True, null=True)
    process_received_datetime = models.DateTimeField(blank=True, null=True)

    parts = models.ForeignKey(Part, on_delete=models.CASCADE)
    client = models.ForeignKey("client.Client", on_delete=models.CASCADE, null=True)
    weight = models.FloatField()
    phone = models.CharField(max_length=255, blank=True, null=True)
    delivery_point = models.PointField(blank=True, null=True)

    @property
    def delivery_price(self):
        return self.parts.country.price_per * self.weight

    @property
    def facture_price(self):
        return ProductInOrder.objects.filter(order=self).annotate(
            _tp=ProductInOrder.annotate_total_price()
        ).aggregate(_tp__sum=models.Sum("_tp")).get("_tp__sum")

    @classmethod
    def status_sql(cls):
        return models.Case(
            models.When(process_received_datetime__isnull=False, then=models.Value("process_received_datetime")),
            models.When(process_local_datetime__isnull=False, then=models.Value("process_local_datetime")),
            models.When(process_customs_datetime__isnull=False, then=models.Value("process_customs_datetime")),
            models.When(enter_uzb_datetime__isnull=False, then=models.Value("enter_uzb_datetime")),
            models.When(departure_datetime__isnull=False, then=models.Value("departure_datetime")),
            default=models.Value("create_time"),
        )

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
        elif self.departure_datetime:
            return 'departure_datetime'
        return 'create_time'

    @property
    def serialized_data(self):
        return {
            "shipmentId": str(self.id),
            "shipmentNumber": str(self.number),
            "shipmentIdCreatTime": self.create_time.timestamp(),
            "shipmentOrgName": str(self.parts.country.company.name),
            "shipmentOrgStir": str(self.parts.country.company.stir),
            "shipmentCountryCode": str(self.parts.country.code),
            "shipmentCountry": str(self.parts.country.name),
            "shipmentSendOrg": str(self.parts.country.send_org),
            "shipmentDepartureTime": self.departure_datetime.timestamp() if self.departure_datetime else None,
            "shipmentEnterUzb": self.enter_uzb_datetime.timestamp() if self.enter_uzb_datetime else None,
            "shipmentProcessCustoms": self.process_customs_datetime.timestamp() if self.process_customs_datetime else None,
            "shipmentProcessLocal": self.process_local_datetime.timestamp() if self.process_local_datetime else None,
            "shipmentReceivedInd": self.process_received_datetime.timestamp() if self.process_received_datetime else None,
        }

    def send_ws_data(self, user_id):
        from .api_admin.serializers import OrderSerializer

        send_data_to_session(user_id, OrderSerializer(self).data)

    def send_api_customs_data(self, systems: list[str] = None):
        systems = list(System.objects.filter(active=True, company=self.parts.country.company).values_list("system_name", flat=True)) \
            if not systems else systems
        _send_api_customs_data.delay(str(self.id), systems, sub=self.parts.country.company.sub)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = _generate_order_number(self)
        return super(Order, self).save(*args, **kwargs)


@shared_task(bind=True)
def _send_api_customs_data(self, order_id, systems, sub):
    order = Order.objects.select_related("parts", "parts__country", "client", "parts__country__company").get(id=order_id)
    api = ApiPushService(sub, order.parts.country.company.private_key)
    json = order.serialized_data
    response = api.create_or_update(self.request.id, json, systems)
    return {"id": str(order.id), "response": response.text, "status": response.status_code, "data": json}


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()

    def __str__(self):
        return self.name


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()

    @classmethod
    def annotate_total_price(cls):
        return models.F('product__price') * models.F('count')

    @property
    def total_price(self):
        return self.product.price * self.count
