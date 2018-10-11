from django.db import models
from django.contrib.auth.models import AbstractUser


class UserTypes:
    COMPANY = 1
    CUSTOMER = 2
    INVESTOR = 3


class ReviewTypes:
    COMPANY = 1
    PRODUCT = 2


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

    def get_products(self):
        return Product.objects.filter(company=self.id)

    def get_reviews(self):
        return Review.objects.filter(company=self.id)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return u'{0}'.format(self.name)


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField()
    price = models.FloatField()

    def get_reviews(self):
        return Review.objects.filter(product=self.id)


class Review(models.Model):
    REVIEW_TYPE_CHOICES = (
        (ReviewTypes.COMPANY, 'company'),
        (ReviewTypes.PRODUCT, 'product'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=1024)
    review_type = models.PositiveSmallIntegerField(choices=REVIEW_TYPE_CHOICES)
