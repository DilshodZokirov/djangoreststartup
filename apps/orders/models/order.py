from django.db import models

from apps.product.models import Product
from apps.users.models import User
from distributive.models import BaseModel


class OrderProduct(BaseModel):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,
                                blank=True)
    count = models.IntegerField(default=1)
    price = models.FloatField(default=0)

    # @property
    # def total_price(self):
    #     return float(self.count) * float(self.price)


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
    products = models.ManyToManyField(Product, through=OrderProduct, related_name="order_products")

    def __str__(self):
        return self.customer_name
