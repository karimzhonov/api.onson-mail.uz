from django.contrib import admin

from cargo.order.models import Order, Country, Part


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ['number', 'country']

    def save_model(self, request, obj: Part, form, change):
        super().save_model(request, obj, form, change)
        if 'status' in form.changed_data:
            obj.send_api_customs_data()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'client', 'parts']
    readonly_fields = [
        'departure_datetime', 'enter_uzb_datetime', 'process_local_datetime',
        'process_customs_datetime', 'process_received_datetime', 'create_time'
    ]
