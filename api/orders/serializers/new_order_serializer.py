from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import Serializer, ModelSerializer

from apps.orders.models import Order, OrderItem
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
class ProductSerializer(ModelSerializer):
    # name = models.CharField(max_length=300)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_product", null=True, blank=True)
    # price1 = models.FloatField(null=True, blank=True)
    # price2 = models.FloatField(null=True, blank=True)
    # compound = models.CharField(max_length=5000, null=True)
    # temporarily_unavailable = models.BooleanField(default=False)
    # temporarily = models.CharField(max_length=5000, null=True, blank=True)
    # pictures = models.FileField(upload_to='product', null=True, blank=True)
    # expiration_date = models.DateTimeField()
    # count = models.IntegerField(null=True, blank=True)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    # size = models.IntegerField(null=True, blank=True)
    # count_of_product = models.IntegerField(null=True, blank=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price1",
            "price2",
            "compound",
            "temporarily_unavailable",
            "temporarily",
            "pictures",
            "expiration_date",
            "count",
            "size",
            "count_of_product",
        ]


# class GroupCreateSerializer(ModelSerializer):
#      memberships = GroupMembershipSerializer(many=True, required=False)
#
#
#
#
class OrderProductSerializer(ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(required=True, queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "count",
            'price'
        ]


class ProductGetSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class ProductAllSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "product",
            "count",
            'price'
        ]


class GetAllOrderSerializers(ModelSerializer):
    products = ProductAllSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "pharmacy_name",
            "customer_name",
            "phone_number",
            "seller",
            "comment",
            "products",
            "total_price",
            "paid_price",
            "inn"
        ]


class NewOrderCreateSerializer(ModelSerializer):
    products = OrderProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = [
            "products",
            "seller",
            "pharmacy_name",
            "customer_name",
            "phone_number",
            "total_price",
            "paid_price",
            'inn',
            "comment",
        ]

    def create(self, validated_data):
        order_data = validated_data.pop('products')
        validated_data['seller'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        for person in order_data:
            d = dict(person)
            order_item = OrderItem.objects.create(product=d.get('product'), count=d.get('count'),
                                                  price=d.get('price'))
            order_item.save()
        return order

    def update(self, instance, validated_data):
        order_data = validated_data.pop('order_products')
        for item in validated_data:
            if Order._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        OrderProduct.objects.filter(order=instance).delete()
        for person in order_data:
            d = dict(person)
            OrderItem.objects.create(order=instance, product=d.get('product'), count=d.get('count'),
                                     price=d.get('price'))
        instance.save()
        return instance


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
        model = OrderItem
        fields = [
            "order",
            "product",
            "count"
        ]


class UpdateOrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
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
