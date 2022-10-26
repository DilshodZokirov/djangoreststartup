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
            "phone_number"
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

    def create(self, validated_data):
        seller = self.context['request'].user
        order = Order.objects.create(
            seller=seller
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
