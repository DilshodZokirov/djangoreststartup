from django.db import transaction
from django.db.models import Q
from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from apps.users.models import User, District

choices = (
    ("AGENT", "agent"),
    ("MANAGER", "manager"),
    ("DELIVERY", "delivery")
)


class GetAllSerializer(ModelSerializer):
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


class DistrictUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            "name"
        ]


class DetailUserCompanySerializer(serializers.ModelSerializer):
    district = DistrictUserSerializer()

    class Meta:
        model = User
        fields = [
            "district",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "email",
            "date_joined"
        ]


class MemberUpdateSerializer(serializers.ModelSerializer):
    profile_pic = serializers.FileField(required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    role = serializers.ChoiceField(required=False)

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

    def update(self, instance, validated_data):
        instance.save()
        return {"message": {
            "uz": "muoffaqiyatli o'zgartirildi",
            "en": "Successfully update",
            "ru": "Создано успешно"
        }}


class MemberAllSerializer(serializers.ModelSerializer):
    district = DistrictUserSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            "district",
            "first_name",
            "last_name",
            "phone_number"
        ]


class UserCreateSerializer(serializers.ModelSerializer):
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
            raise ValidationError(
                {
                    "uz": "Bunday ishchi  korxonada ishlaydi  !!!",
                    "en": "Such an employee works in an enterprise !!",
                    "ru": "Такой сотрудник работает на предприятии !!"
                })
        if len(password) < 6:
            raise ValidationError(
                {
                    "uz": "Iltimos passwordni 6 ta belgidan ko'proq kiriting !!!",
                    "en": "Please enter password with more than 6 characters !!!",
                    "ru": "Пожалуйста, введите пароль длиной более 6 символов !!!"
                })
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
            user.phone_number = validated_data.get("phone_number")
            user.save()
        else:
            validated_data['company'] = company
            validated_data['role'] = validated_data.get("role")
            User.objects.create_user(
                **validated_data
            )
        return {
            "uz": "Muvaffaqiyatli yaratildi !!!",
            "en": "Successfully Created !!!",
            "ru": "Создано успешно !!!",
        }


class DistrictClassMemberSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = [
            "id",
            "name"
        ]
