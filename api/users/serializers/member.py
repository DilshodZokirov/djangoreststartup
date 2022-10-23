from django.db import transaction
from django.db.models import Q
from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from apps.users.models import User, District

choices = (
    ("AGENT", "agent"),
    ("MANAGER", "manager"),
    ("DELIVERY", "delivery")
)


class GetAllSerializer(Serializer):
    class Meta:
        fields = [
            'district',
            'profile_pic',
            'username',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'role',
            'password',
        ]


class UserCreateSerializer(Serializer):
    # class Choices(models.Choices):

    profile_pic = serializers.FileField(required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    role = serializers.ChoiceField(required=False, choices=choices, default="DELIVERY")

    class Meta:
        model = User
        fields = [
            'district',
            'profile_pic',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'role',
            'password',
        ]

    def validate(self, attrs: dict):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        if User.objects.filter(Q(phone_number=phone_number) & ~Q(role="unemployed")).exists():
            raise ValidationError("Bunday ishchi boshqa korxonada ishlaydi bor !!!")
        if len(password) < 6:
            raise ValidationError("Iltimos passwordni 6 ta belgidan ko'proq kiriting !!!")
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict):
        company = self.context['request'].user.company
        if User.objects.filter(Q(phone_number=validated_data.get("phone_number")) & Q(role="unemployed")).exists():
            user = User.objects.get(Q(phone_number=validated_data.get("phone_number")) & Q(role="unemployed"))
            user.district = validated_data.get("district")
            user.first_name = validated_data.get("first_name")
            user.last_name = validated_data.get("last_name")
            user.date_of_birth = validated_data.get("date_of_birth")
            user.role = validated_data.get("role")
            user.date_of_birth = validated_data.get("date_of_birth")
            user.phone_number = validated_data.get("phone_number")
            user.save()
        else:
            validated_data['company'] = company
            validated_data['role'] = validated_data.get("role")
            User.objects.create_user(
                **validated_data
            )
        return {"message": "Success"}
