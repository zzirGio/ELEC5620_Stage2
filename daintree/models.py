from django.db import models
from django.contrib.auth.models import AbstractUser


class UserTypes:
    COMPANY = 1
    CUSTOMER = 2
    INVESTOR = 3


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (UserTypes.COMPANY, 'company'),
        (UserTypes.CUSTOMER, 'customer'),
        (UserTypes.INVESTOR, 'investor')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.email


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    address = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    nb_employees = models.IntegerField(default=0)
    owner = models.CharField(max_length=255)
    ethereum_pk = models.CharField(max_length=255, null=True, blank=True)
