from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import MerchantManager


class Merchant(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MerchantManager()

    def __str__(self):
        return self.email

    def to_dict(self):
        return {
            'email': self.email,
            'name': self.first_name + self.last_name
        }
