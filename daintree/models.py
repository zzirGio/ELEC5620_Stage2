from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from aylienapiclient import textapi

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
        return Product.objects.filter(company=self)

    def get_reviews(self):
        return Review.objects.filter(company=self, review_type=ReviewTypes.COMPANY)

    def __str__(self):
        return u'{}, {}, {}, {}'.format(self.user_id, self.address, self.description, self.owner)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return u'{0}'.format(self.name)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return u'{}'.format(self.user_id)


class Investor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    fundId = models.CharField(max_length=32)

    def __str__(self):
        return u'{}, {}'.format(self.user_id, self.fundId)


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.IntegerField()
    price = models.FloatField()
    description = models.CharField(max_length=1024, null=True, blank=True)

    def get_reviews(self):
        return Review.objects.filter(product=self, review_type=ReviewTypes.PRODUCT, company=self.company)

    def __str__(self):
        return u'{}, {}, {}, {}'.format(self.company, self.name, self.category, self.price)


class Review(models.Model):
    REVIEW_TYPE_CHOICES = (
        (ReviewTypes.COMPANY, 'company'),
        (ReviewTypes.PRODUCT, 'product'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    review_type = models.PositiveSmallIntegerField(choices=REVIEW_TYPE_CHOICES)

    def __str__(self):
        return u'{}, {}, {}'.format(self.content, self.review_type, self.company)


class SentimentResult:
    def __init__(self, sentiment='Neutral', confidence=0.0):
        self.sentiment = sentiment
        self.confidence = confidence


class SentimentAnalysis():
    client = textapi.Client(settings.AYLIEN_APP_ID, settings.AYLIEN_KEY)

    def analyse(self, reviews):
        contents = []
        for review in reviews:
            contents.append(review.content)

        sentiment = self.client.Sentiment({'text': ' '.join(contents)})

        return SentimentResult(sentiment['polarity'], sentiment['polarity_confidence'])
