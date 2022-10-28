from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from apps.orders.models import Order, OrderProduct
from apps.product.models import Product
from apps.users.models import User


class SellerClassesSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]


class GetOneOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "order_position",
            "pharmacy"
        ]


class OrderClassesSerializer(ModelSerializer):
    seller = SellerClassesSerializer()

    class Meta:
        model = Order
        fields = [
            "pharmacy_name",
            "customer_name",
            "seller",
            "phone_number",
            "created_date",
        ]


#
# class NewOrderSerializer(Serializer):
#     pharmacy_name = serializers.CharField(max_length=400)
#     phone_number = serializers.CharField(max_length=20)
#     customer_name = serializers.CharField(max_length=70)
#     comment = serializers.CharField(max_length=500)
#
#     class Meta:
#         model = Order
#         fields = [
#             "pharmacy_name",
#             "phone_number",
#             "customer_name",
#             "comment",
#         ]
#
#     def create(self, validated_data):
#         seller = self.context['request'].user
#

# Order Product Serializers
class CreateOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id"
        ]

    def create(self, validated_data):
        seller = self.context['request'].user.id
        order = Order.objects.create(
            seller_id=seller
        )
        order.save()
        return {"success"}


class CreateOrderProductSerializer(ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_deleted=False))
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.filter(is_deleted=False))

    class Meta:
        model = OrderProduct
        fields = [
            "order",
            "product",
            "count"
        ]


class UpdateOrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = [
            "order",
            "product"
        ]


class UpdateOrderSerializer(ModelSerializer):
    pharmacy_name = serializers.CharField(required=False, max_length=70)
    customer_name = serializers.CharField(required=False, max_length=80)
    phone_number = serializers.CharField(required=False, max_length=40)
    comment = serializers.CharField()

    class Meta:
        model = Order
        fields = [
            "pharmacy_name",
            "customer_name",
            "phone_number",
            "comment",
        ]

    def update(self, instance: Order, validated_data: dict):
        summa = 0
        order_id = instance.pk
        order_product = OrderProduct.objects.filter(order_id=order_id)
        for op in order_product:
            summa += op.price
        instance.seller = self.context['request'].user
        instance.customer_name = validated_data.get('customer_name')
        instance.phone_number = validated_data.get('phone_number')
        instance.comment = validated_data.get("comment")
        instance.pharmacy_name = validated_data.get("pharmacy_name")
        instance.total_price = summa
        instance.comment = validated_data.get("comment")
        instance.save()
        return {
            "success"
        }
