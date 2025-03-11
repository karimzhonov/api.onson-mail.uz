from django.contrib import admin
from import_export.admin import ImportMixin
from cargo.order.models import Order, Part, ProductInOrder, Product
from .resources import ProductResource, OrderResource
from .formats import OrderXLSX
from .forms import OrderConfirmImportForm, OrderImportForm


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
class OrderAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['number', 'client', 'parts']
    list_filter = ['client', 'parts']
    readonly_fields = [
        'departure_datetime', 'enter_uzb_datetime', 'process_local_datetime',
        'process_customs_datetime', 'process_received_datetime', 'create_time'
    ]
    actions = ['send_api_customs_data']
    inlines = [ProductInOrderTabular]

    import_form_class = OrderImportForm
    confirm_form_class = OrderConfirmImportForm
    resource_classes = [OrderResource]
    # form = OrderForm
    skip_admin_log = True
    formats = [OrderXLSX]

    def send_api_customs_data(self, request, queryset):
        for order in queryset:
            order.send_api_customs_data()

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        if import_form is None:
            return initial
        initial["part"] = request.POST.get("part")
        return initial
    
    def get_import_data_kwargs(self, request, *args, **kwargs):
        kwargs.update(form_data=kwargs.get("form").cleaned_data)
        return super().get_import_data_kwargs(request, *args, **kwargs)

@admin.register(Product)
class ProductAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['name', 'price']
    resource_classes = [ProductResource]