from django.db import models

from apps.product.models import Product
from apps.users.models import User, Company
from distributive.models import BaseModel


class Order(BaseModel):
    class OrderPosition(models.TextChoices):
        PENDING = "Pending"
        BASKET = "Basket"
        VERIFICATION = "Verification"
        DELIVERY = "Delivery"
        FINISH = "Finish"

    class MoneyPaid(models.TextChoices):
        NOT_PAID = "not_paid"
        ORPHAN_PAID = "orphan_paid"
        FULL_PAID = "full_paid"

    pharmacy_name = models.CharField(max_length=30, null=True, blank=True)
    customer_name = models.CharField(max_length=300, null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_seller', null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    paid_price = models.FloatField(null=True, blank=True, default=0)
    total_price = models.FloatField(null=True, blank=True, default=0)
    paid_position = models.CharField(max_length=30, choices=MoneyPaid.choices, default=MoneyPaid.NOT_PAID)
    order_position = models.CharField(max_length=400, choices=OrderPosition.choices, default=OrderPosition.PENDING)
    comment = models.CharField(max_length=500, null=True, blank=True)
    products = models.ManyToManyField("OrderItem", related_name="order_products")
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL)
    lon = models.CharField(max_length=400, null=True, blank=True)
    lot = models.CharField(max_length=400, null=True, blank=True)
    inn = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.customer_name


class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name="order_product_order", on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    def __str__(self):
        return f"{self.product.name} of {self.count}"
