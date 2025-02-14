# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class OrdersOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.IntegerField(blank=True, null=True)
    clientid = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    weight = models.FloatField()
    facture_price = models.FloatField()
    client = models.ForeignKey('UsersClient', models.DO_NOTHING, to_field='pnfl')
    part = models.ForeignKey('OrdersPart', models.DO_NOTHING)
    date = models.DateTimeField(blank=True, null=True)
    products = models.JSONField()
    with_online_buy = models.BooleanField()
    dates = models.JSONField()
    uuid = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders_order'


class OrdersPart(models.Model):
    id = models.BigAutoField(primary_key=True)
    number = models.IntegerField()
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'orders_part'


class UsersClient(models.Model):
    id = models.BigAutoField(primary_key=True)
    pnfl = models.CharField(unique=True, max_length=255)
    passport = models.CharField(unique=True, max_length=255)
    fio = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, blank=True, null=True)
    passport_image = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'users_client'

