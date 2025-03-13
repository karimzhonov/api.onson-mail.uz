from django.contrib import admin

from cargo.models import CargoUser


@admin.register(CargoUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'user']
