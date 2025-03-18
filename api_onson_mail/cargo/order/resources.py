from django.db.models import Q
from django.core.exceptions import ValidationError
from import_export import resources

from cargo.client.models import Client

from .models import Order, Product, ProductInOrder


class OrderResource(resources.ModelResource):
    number = resources.Field(column_name='4', attribute='number')
    client = resources.Field(column_name='5', attribute='client')
    weight = resources.Field(column_name='13', attribute='weight')
    products = resources.Field(column_name='12', attribute='products')

    class Meta:
        model = Order
        fields = "__all__"
        import_id_fields = ["number"]

    def import_field(self, field: resources.Field, instance, row, is_m2m=False, **kwargs):
        if field.attribute == 'number':
            instance.parts = kwargs.get('form_data').get('part')
            instance.number = row.get(field.column_name)
            return
        if field.attribute == 'client':
            client = Client.objects.filter(Q(pnfl=row.get('8')) | Q(passport=row.get('6')) | Q(passport=row.get('5'))).first()
            if not row.get('6') or not row.get('8') or not row.get('5'): return
            if not client:
                client = Client.objects.create(**{
                    "pnfl": row.get('8'),
                    "passport": row.get('6'),
                    "fio": row.get("5"),
                    "address": row.get("10"),
                    "created_user_id": kwargs.get('user').id
                })
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
        if field.attribute == 'products':
            products = str(row.get(field.column_name)).split(", ")
            for product in products:
                try:
                    price = float(product.split(" ")[-1])
                except ValueError:
                    price = 0
                p, c = Product.objects.get_or_create({"price": price}, name=product)
                ProductInOrder.objects.create(
                    order=instance, product=p, count=price
                )
            return
        raise NotImplemented

    def import_obj(self, obj, data, dry_run, **kwargs):
        obj.save()
        return super().import_obj(obj, data, dry_run, **kwargs)

    def skip_row(self, instance: Order, *args, **kwargs):
        if not instance.client: return True


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        fields = ['name', 'price']
        import_id_fields = ["name"]
