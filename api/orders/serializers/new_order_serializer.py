from rest_framework.serializers import Serializer

from apps.orders.models import Order
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


class OrderClassesSerializer(Serializer):
    seller = SellerClassesSerializer()

    class Meta:
        model = Order
        fields = [
            "pharmacy_name",
            "seller",
            "phone_number",
            "paid_price",
            "total_price",
            "paid_position",
            "order_position"
        ]
