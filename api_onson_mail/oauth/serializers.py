from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.serializerfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'avatar')


class OptSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    user = UserShortSerializer(read_only=True)

    def create(self, validated_data):
        phone = validated_data.get('phone')
        user, created = User.objects.get_or_create(phone=phone)
        if created:
            user.set_unusable_password()
        user.send_opt(True)
        return {"phone": phone, "user": user}

class OptVerifySerializer(serializers.Serializer):
    phone = PhoneNumberField(write_only=True)
    opt = serializers.CharField(write_only=True)
    has_usable_password = serializers.BooleanField(read_only=True, required=False)
    success = serializers.BooleanField(read_only=True)
    user = UserShortSerializer(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def validate(self, attrs):
        authenticate_kwargs = {
            "phone": attrs["phone"],
            "opt": attrs["opt"],
        }
        user = User.objects.filter(**authenticate_kwargs).first()

        if not user or not api_settings.USER_AUTHENTICATION_RULE(user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {
            "user": user,
            "success": True,
            "has_usable_password": user.has_usable_password(),
        }

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)

        validated_data["refresh"] = str(refresh)
        validated_data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
        print(validated_data)
        return validated_data


class SignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "password1", "password2", "avatar"]

    def validate(self, attrs):
        password = attrs.pop("password1", None)
        password2 = attrs.pop("password2", None)
        if password:
            if password != password2:
                raise serializers.ValidationError(
                    _("Passwords don't match"),
                    code='passwords-do-not-match'
                )
            validate_password(password)
            attrs["password"] = password
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get("password1"):
            instance.set_password(validated_data.pop("password"))
        return super().update(instance, validated_data)
