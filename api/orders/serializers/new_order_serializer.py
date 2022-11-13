from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer

from apps.orders.models import Order, OrderProduct
from apps.product.models import Product
from apps.users.models import User


class SellerClassesSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
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
            "pharmacy_name"
        ]


class DetailOrderSerializer(ModelSerializer):
    seller = SellerClassesSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "created_date",
            "updated_date",
            "pharmacy_name",
            "customer_name",
            "phone_number",
            "seller",
            "comment"
        ]


class OrderClassesSerializer(ModelSerializer):
    seller = SellerClassesSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
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
# class ProductSerializer(ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "name",
#             "count_of_product",
#             "size",
#             "count"
#         ]


# class GroupCreateSerializer(ModelSerializer):
#      memberships = GroupMembershipSerializer(many=True, required=False)
#
#
#
#
class OrderProductSerializer(ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = [
            "product",
            "count",
            'price'
        ]


class NewOrderCreateSerializer(ModelSerializer):
    products = OrderProductSerializer(many=True, required=False)

    # pharmacy_name = models.CharField(max_length=30, null=True, blank=True)
    # customer_name = models.CharField(max_length=300, null=True, blank=True)
    # seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_seller', null=True, blank=True)
    # phone_number = models.CharField(max_length=50, null=True, blank=True)
    # paid_price = models.FloatField(null=True, blank=True, default=0)
    # total_price = models.FloatField(null=True, blank=True, default=0)
    # paid_position = models.CharField(max_length=30, choices=MoneyPaid.choices, default=MoneyPaid.NOT_PAID)
    # order_position = models.CharField(max_length=400, choices=OrderPosition.choices, default=OrderPosition.PENDING)
    # comment = models.CharField(max_length=500, null=True, blank=True)
    # products =
    class Meta:
        model = Order
        fields = [
            "products",
            "seller",
            "pharmacy_name",
            "customer_name",
            "phone_number",
            "comment",
        ]

    def create(self, validated_data):
        order_data = validated_data.pop('products')
        validated_data['seller'] = self.context['request'].get('user')
        order = Order.objects.create(**validated_data)
        for person in order_data:
            d = dict(person)
            OrderProduct.objects.create(order=order, product=d.get('product'), count=d.get('count'),
                                        price=d.get('price'))
        return order

    def update(self, instance, validated_data):
        order_data = validated_data.pop('order_products')
        for item in validated_data:
            if Order._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        OrderProduct.objects.filter(order=instance).delete()
        for person in order_data:
            d = dict(person)
            OrderProduct.objects.create(order=instance, product=d.get('product'), count=d.get('count'),
                                        price=d.get('price'))
        instance.save()
        return instance


class Meta:
    pass


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
