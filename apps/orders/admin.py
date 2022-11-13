from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.orders.models import Order, OrderProduct


# pharmacy_name = models.CharField(max_length=30, null=True, blank=True)
#     customer_name = models.CharField(max_length=300, null=True, blank=True)
#     seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_seller', null=True, blank=True)
#     phone_number = models.CharField(max_length=50, null=True, blank=True)
#     paid_price = models.FloatField(null=True, blank=True, default=0)
#     total_price = models.FloatField(null=True, blank=True, default=0)
#     paid_position = models.CharField(max_length=30, choices=MoneyPaid.choices, default=MoneyPaid.NOT_PAID)
#     order_position = models.CharField(max_length=400, choices=OrderPosition.choices, default=OrderPosition.PENDING)
#     comment = models.CharField(max_length=500, null=True, blank=True)
@admin.register(Order)
class AdminOrder(ModelAdmin):
    list_display = ["id", "pharmacy_name", "customer_name", "phone_number"]


@admin.register(OrderProduct)
class AdminOrderProduct(ModelAdmin):
    list_display = ["id", "order", "product", "price"]
