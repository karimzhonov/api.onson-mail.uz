import os
import requests
from django.core.management import BaseCommand
from django.db.transaction import atomic
from django.db.utils import IntegrityError
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import File
from django.contrib.auth.hashers import make_password
from phonenumber_field.phonenumber import PhoneNumber
from cargo.order.old import OrdersPart, UsersClient, OrdersOrder
from cargo.models import CargoUser
from cargo.order import models
from cargo.client.models import Client
from oauth.models import User


class Command(BaseCommand):

    def parts(self):
        country_id = 1

        for part in OrdersPart.objects.using('old').values_list("number", flat=True):
            models.Part.objects.get_or_create({
                'country_id': country_id,
                'status': models.STATUSES[-1][0]
            }, number=part)
            print('Part', part)

    def clients(self):
        for client in UsersClient.objects.using('old').all():
            if not len(client.pnfl) == 14:
                continue
            user = None
            print('Client', client)
            if client.phone:
                phone = client.phone.replace(' ', '').replace('-', '').split('/')[0]
                if len(client.phone) == 9:
                    phone = f"+998{phone}"
                try:
                    phone = PhoneNumber.from_string(phone)
                except:
                    phone = PhoneNumber.from_string(f"+998{phone[:9]}")
                user, _ = User.objects.get_or_create({
                    'first_name': client.fio, "password": make_password(None)
                }, phone=phone)
                
            # if client.passport_image and user:
            #     url = f"http://178.208.75.215/media/{client.passport_image}"
            #     r = requests.get(url)
            #     if r.status_code == 200:
            #         img_temp = NamedTemporaryFile(delete=True)
            #         img_temp.write(r.content)
            #         img_temp.flush()

            #         user.avatar.save(os.path.basename(client.passport_image), File(img_temp), save=True)
            client, _ = Client.objects.get_or_create({
                "passport": client.passport,
                "fio": client.fio,
                "address": client.address,
            }, pnfl=client.pnfl)
            if user:
                cu, _ = CargoUser.objects.get_or_create(user=user)
                cu.clients.add(client)


    def orders(self):
        for order in OrdersOrder.objects.using('old').all().prefetch_related('part'):
            client = Client.objects.filter(pnfl=order.client_id).first()
            if not client: continue
            print(order)
            models.Order.objects.get_or_create(
                {
                    "create_time":order.date,
                    "departure_datetime":order.date,
                    "enter_uzb_datetime":order.date,
                    "process_customs_datetime":order.date,
                    "process_local_datetime":order.date,
                    "process_received_datetime":order.date,
                    "parts_id":order.part.number,
                    "client":client,
                    "name":order.name,
                    "weight":order.weight,
                    "facture_price":order.facture_price
                },
                number=order.number,
            )


    @atomic
    def handle(self, *args, **options):
        self.parts()
        self.clients()
        self.orders()