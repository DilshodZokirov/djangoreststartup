from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from apps.users.models import User, Company


class LoginUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "password"
        ]

    def validate(self, attrs):
        if attrs.get('phone_number') and attrs.get('password'):
            request = self.context['request']
            user = authenticate(request, phone_number=attrs.get('phone_number'), password=attrs.get('password'))
            if not user:
                raise serializers.ValidationError('User is not found')
            token, _ = Token.objects.get_or_create(user=user)
            attrs['user'] = user
            attrs['token'] = token
        return attrs


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()
    password2 = serializers.CharField()
    company = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            'company',
            "phone_number",
            "password",
            "password2"
        ]
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def validate(self, attrs: dict):
        phone_number = attrs.get('phone_number')
        user_name = attrs.get("username")
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(
                "Bunaqa telefon nomerli inson bizda bor iltimos boshqa nomerdan foydalaning yoki login qismiga o'ting !!!")
        if 10 >= len(phone_number) >= 12:
            raise ValidationError("Iltimos telefon nomerni to'g'ri kiriting !!!")
        if attrs.get('password') != attrs.get("password2"):
            raise ValidationError("Iltimos parolni to'g'ri kiriting !!!")
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Bunaqa inson bizning ro'yxatda bor")
        if Company.objects.filter(name=attrs.get("company")).exists():
            raise ValidationError("Bunday Company bizda bor iltimos boshqa nom qo'ying !!!")
        if User.objects.filter(username=user_name).exists():
            raise ValidationError("Bunday nom mavjud !!!")
        return attrs

    @transaction.atomic
    def create(self, validated_data: dict):
        username = validated_data.get("username")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")
        password = validated_data.get("password")
        phone_number = validated_data.get('phone_number')
        company_name = validated_data.get("company")
        company = Company.objects.create(name=company_name)
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number,
            company=company,
            role="office_manager",
            is_director=True
        )
        company.created_by = user
        company.save()
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'role',
        ]
