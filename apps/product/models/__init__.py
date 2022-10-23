from django.db import models
from distributive.models import BaseModel
from apps.users.models import Company


class Product(BaseModel):
    name = models.CharField(max_length=300)
    price1 = models.FloatField(null=True, blank=True)
    price2 = models.FloatField(null=True, blank=True)
    compound = models.CharField(max_length=5000, null=True)
    temporarily_unavailable = models.BooleanField(default=False)
    pictures = models.FileField(upload_to='product', null=True, blank=True)
    expiration_date = models.DateTimeField()
    count = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    count_of_product = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
