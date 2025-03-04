from django.contrib import admin
from import_export.admin import ImportMixin
from cargo.order.models import Order, Part, ProductInOrder, Product
from .resources import ProductResource


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['number', 'country']

    def save_model(self, request, obj: Part, form, change):
        super().save_model(request, obj, form, change)
        if 'status' in form.changed_data:
            obj.send_api_customs_data()

class ProductInOrderTabular(admin.TabularInline):
    model = ProductInOrder
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'client', 'parts']
    readonly_fields = [
        'departure_datetime', 'enter_uzb_datetime', 'process_local_datetime',
        'process_customs_datetime', 'process_received_datetime', 'create_time'
    ]
    actions = ['send_api_customs_data']
    inlines = [ProductInOrderTabular]

    def send_api_customs_data(self, request, queryset):
        for order in queryset:
            order.send_api_customs_data()

@admin.register(Product)
class ProductAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['name', 'price']
    resource_classes = [ProductResource]