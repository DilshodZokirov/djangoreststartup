from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import Serializer

from apps.product.models import Product


#     name = models.CharField(max_length=300)
#     price1 = models.FloatField(null=True, blank=True)
#     price2 = models.FloatField(null=True, blank=True)
#     compound = models.CharField(max_length=5000, null=True)
#     temporarily_unavailable = models.BooleanField(default=False)
#     pictures = models.FileField(upload_to='product', null=True, blank=True)
#     expiration_date = models.DateTimeField()
#     count = models.IntegerField(null=True, blank=True)
#     count_of_product = models.IntegerField(null=True, blank=True)
class AgentProductSerializer(Serializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "price1",
            "price1",
            "compound",
            'temporarily_unavailable',
            'pictures',
            "expiration_date",
            "count",
            "size",
            "count_of_product"
        ]


class DetailProductSerializer(Serializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "price1",
            "price1",
            "compound",
            'temporarily_unavailable',
            'pictures',
            "expiration_date",
            "count",
            "size",
            "count_of_product"
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    pictures = serializers.FileField(required=False)
    name = serializers.CharField(required=False)
    price1 = serializers.FloatField(required=False)
    price2 = serializers.FloatField(required=False)
    compound = serializers.CharField(required=False)
    expiration_date = serializers.DateTimeField(required=True)

    class Meta:
        model = Product
        fields = [
            'pictures',
            'name',
            'category',
            'price1',
            'price2',
            'compound',
            'expiration_date',
            'temporarily_unavailable',
        ]

    @transaction.atomic
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        if self.data.get('temporarily_unavailable'):
            validated_data['temporarily_unavailable'] = self.data.get('temporarily_unavailable')
        else:
            validated_data['temporarily_unavailable'] = False
        Product.objects.create(**validated_data)
        return {
            "uz": "Muvaffaqiyatli yaratildi !!!",
            "en": "Successfully Created",
            "ru": "Создано успешно"
        }
