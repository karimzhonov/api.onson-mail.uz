from django.contrib import admin

from cargo.models import CargoUser


@admin.register(CargoUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'user']
    search_fields = ["user__first_name", "user__phone"]

