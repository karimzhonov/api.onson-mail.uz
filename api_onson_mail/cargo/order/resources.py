from django.core.exceptions import ValidationError
from import_export import resources

from cargo.client.models import Client

from .models import Order, Product


class OrderResource(resources.ModelResource):
    # part = resources.Field("part__number")
    # passport = resources.Field("client__passport", readonly=True)
    number = resources.Field(column_name='1. Тижорат хужжатининг раками', attribute='number')
    clientid = resources.Field(column_name='2. Халкаро курьерлик жунатмасининг жунатувчиси', attribute='clientid')
    name = resources.Field(column_name='3. Халкаро курьерлик жунатмасининг кабул килувчиси ва унинг манзили', attribute='name')
    client = resources.Field(column_name='4. Халкаро курьерликнинг жунатмасидаги товарларнинг кискача номи', attribute='client')
    weight = resources.Field(column_name='5. Халкаро курьерлик жунатмасининг брутто вазни (кг)', attribute='weight')
    facture_price = resources.Field(column_name='6. Халкаро курьерлик жунатмасининг фактура киймати', attribute='facture_price')

    class Meta:
        model = Order
        exclude = ["products", "id", "with_online_buy"]
        import_id_fields = ["number"]

    def import_field(self, field, instance, row, is_m2m=False, **kwargs):
        if field.attribute == 'part':
            instance.part = kwargs.get('form_data').get('part')
            return
        if field.attribute == 'date':
            instance.date = kwargs.get('form_data').get('date')
            return
        if field.attribute == 'client':
            try:
                client = Client.objects.get(pnfl=row[field.column_name])
            except Client.DoesNotExist:
                client = Client.objects.create(
                    pnfl=row[field.column_name],
                    passport=row[field.column_name],
                    fio=row[field.column_name],
                )
            instance.client = client
            return
        if field.attribute == 'weight':
            try:
                weight = str(row.get(field.column_name))
                weight = float(weight.replace(",", "."))
                instance.weight = weight
                return
            except ValueError:
                raise ValidationError(message=f"{row.get('weight')} - invalid weight")
        if field.attribute == 'facture_price':
            try:
                facture_price = str(row.get(field.column_name))
                facture_price = float(facture_price.replace(",", "."))
                instance.facture_price = facture_price
            except ValueError:
                raise ValidationError(message=f"{row.get('facture_price')} - invalid price")
        return super().import_field(field, instance, row, is_m2m, **kwargs)


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        fields = ['name', 'price']
        import_id_fields = ["name"]
