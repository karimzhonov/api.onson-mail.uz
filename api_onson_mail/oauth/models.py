from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from .utils import generate_opt

OPT_EXPIRING_LIFESPAN = timedelta(minutes=1)

class User(AbstractUser):
    username = None
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    phone = PhoneNumberField(unique=True)
    opt = models.CharField(max_length=4, null=True, blank=True)
    opt_lia = models.DateTimeField(null=True, blank=True)
    countries = models.ManyToManyField("order.Country", blank=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone)

    @property
    def opt_exp(self):
        now = timezone.now()
        if self.opt_lia < now - OPT_EXPIRING_LIFESPAN:
            return True
        return False

    def opt_check(self, opt):
        return self.opt == opt and not self.opt_exp

    def opt_create(self, save=True):
        self.opt = generate_opt()
        self.opt_lia = timezone.now()
        if save:
            self.save()
        return self.opt

    def send_opt(self, save=True):
        self.opt_create(save)
        print(self.opt, self.phone)
