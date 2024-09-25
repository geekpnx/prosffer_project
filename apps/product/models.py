from django.db import models
from apps.core.constraints import STORE_NAMES
# Create your models here.


class Product(models.Model):
    store = models.CharField(max_length=30, choices=STORE_NAMES)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=150, null=True, blank=True)
    price = models.FloatField()
    currency = models.CharField(max_length=5)
    category = models.CharField(max_length=100, null=True, blank=True)
    image = models.URLField(max_length=255)
    link = models.URLField(max_length=255)
    id_tag = models.CharField(max_length=50, null=True, blank=True) # CharField (encrypt decrypt)

    def __str__(self) -> str:
        return f"Store: {self.store}, Product: {self.name}, Price: {self.price}{self.currency}"