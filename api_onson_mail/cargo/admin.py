from django.contrib import admin

from cargo.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
