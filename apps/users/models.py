from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Profile(AbstractUser):
    phone = PhoneNumberField()
    hobbies = models.TextField(max_length=100, null=True, blank=True)
    validated_email = models.BooleanField(default=False)
    validated_phone = models.BooleanField(default=False)