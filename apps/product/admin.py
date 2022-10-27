from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.product.models import Product


#     name = models.CharField(max_length=300)
#     price1 = models.FloatField(null=True, blank=True)
#     price2 = models.FloatField(null=True, blank=True)
#     compound = models.CharField(max_length=5000, null=True)
#     temporarily_unavailable = models.BooleanField(default=False)
#     pictures = models.FileField(upload_to='product', null=True, blank=True)
#     expiration_date = models.DateTimeField()
#     count = models.IntegerField(null=True, blank=True)
#     size = models.IntegerField(null=True, blank=True)
#     count_of_product = models.IntegerField(null=True, blank=True)

@admin.register(Product)
class ModelAdminProduct(ModelAdmin):
    list_display = [
        "id",
        "name",
        "price1",
        "price2",
        "count",
        "size"
    ]
