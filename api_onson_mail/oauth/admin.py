from django.contrib import admin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission, ContentType

from oauth.models import User

admin.site.register(Permission)
admin.site.register(ContentType)

@admin.register(User)
class UserAdmin(ModelAdmin, _UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("phone", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("phone", "first_name", "last_name", "email")
    ordering = ("phone",)
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "avatar")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "companies",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "password1", "password2"),
            },
        ),
    )