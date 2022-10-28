from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from apps.orders.models import Order, OrderProduct
from apps.product.models import Product
from apps.users.models import User


#     username = models.CharField(max_length=500, null=True, blank=True)
#     phone_number = models.CharField(max_length=13, unique=True)
#     company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True, blank=True, related_name='company')
#     first_name = models.CharField(max_length=400, null=True, blank=True)
#     email = models.EmailField(null=True, blank=True)
#     last_name = models.CharField(max_length=400, null=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True,
#                                  related_name="district_user")
#     profile_pic = models.FileField(upload_to='user/profile', null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=True)
#     is_director = models.BooleanField(default=False)
#     date_of_birth = models.DateField(null=True, blank=True)
#     role = models.CharField(max_length=400, choices=TYPE.choices, default=TYPE.DELIVERY, null=True)
#     is_deleted = models.BooleanField(default=False, null=True, blank=True)

class SellerClassesSerializer(Serializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]


class GetOneOrderSerializer(Serializer):
    class Meta:
        model = Order
        fields = [
            "order_position",
            "pharmacy"
        ]


class OrderClassesSerializer(Serializer):
    seller = SellerClassesSerializer()

    class Meta:
        model = Order
        fields = [
            "pharmacy_name",
            "customer_name",
            "seller",
            "phone_number",
            "created-date",
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
class CreateOrderSerializer(Serializer):
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


class CreateOrderProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_deleted=False))
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.filter(is_deleted=False))

    class Meta:
        model = OrderProduct
        fields = [
            "order",
            "product",
            "count"
        ]


class UpdateOrderProductSerializer(serializers.Serializer):
    class Meta:
        model = OrderProduct
        fields = [
            "order",
            "product"
        ]


#     pharmacy_name = models.CharField(max_length=30, null=True, blank=True)
#     customer_name = models.CharField(max_length=300, null=True, blank=True)
#     seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_seller', null=True, blank=True)
#     phone_number = models.CharField(max_length=50, null=True, blank=True)
#     paid_price = models.FloatField(null=True, blank=True, default=0)
#     total_price = models.FloatField(null=True, blank=True, default=0)
#     paid_position = models.CharField(max_length=30, choices=MoneyPaid.choices, default=MoneyPaid.NOT_PAID)
#     order_position = models.CharField(max_length=400, choices=OrderPosition.choices, default=OrderPosition.PENDING)
#     comment = models.CharField(max_length=500, null=True, blank=True)
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
        return {"success"}
