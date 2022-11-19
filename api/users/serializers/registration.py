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
                raise serializers.ValidationError({"message": {
                    "uz": "Bunaqa inson topilmadi",
                    "ru": "Пользователь не найден",
                    "en": 'User is not found'}})
                token, _ = Token.objects.get_or_create(user=user)
                attrs['user'] = user
                attrs['token'] = token
            return attrs

    class RegistrationSerializer(serializers.ModelSerializer):
        first_name = serializers.CharField(required=False)
        email = serializers.EmailField(required=False)
        password = serializers.CharField()
        password2 = serializers.CharField()
        company = serializers.CharField()

        class Meta:
            model = User
            fields = [
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
            if User.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(
                    {
                        "uz": "Bunaqa telefon nomerli inson bizda bor iltimos boshqa nomerdan foydalaning yoki login qismiga o'ting !!!",
                        "en": "We have a person with such a phone number, please use another number or go to the login section !!!",
                        "ru": "У нас есть человек с таким номером телефона, пожалуйста используйте другой номер или зайдите в раздел авторизации!!!"

                    })
            if 10 >= len(phone_number) >= 12:
                raise ValidationError(
                    {
                        "uz": "Iltimos telefon nomerni to'g'ri kiriting !!!",
                        "en": "Please enter the correct phone number !!!",
                        "ru": "Пожалуйста, введите правильный номер телефона !!!"
                    })
            if attrs.get('password') != attrs.get("password2"):
                raise ValidationError(
                    {
                        "uz": "Iltimos parolni to'g'ri kiriting !!!",
                        "en": "Please enter the correct password !!!",
                        "ru": "Пожалуйста, введите правильный пароль!!!"
                    })
            if User.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(
                    {
                        "uz": "Bunaqa inson bizning ro'yxatda bor",
                        "en": "Such a person is on our list",
                        "ru": "Такой человек есть в нашем списке"
                    })
            if Company.objects.filter(name=attrs.get("company")).exists():
                raise ValidationError(
                    {
                        "uz": "Bunday korxona bizda bor iltimos boshqa nom qo'ying !!!",
                        "en": "We have such a company, please give it another name!!!",
                        "ru": "У нас есть такая компания, дайте ей другое название!!!"
                    }
                )
            return attrs

        @transaction.atomic
        def create(self, validated_data: dict):
            first_name = validated_data.get("first_name")
            last_name = validated_data.get("last_name")
            email = validated_data.get("email")
            password = validated_data.get("password")
            phone_number = validated_data.get('phone_number')
            company_name = validated_data.get("company")
            company = Company.objects.create(name=company_name)
            user = User.objects.create_user(
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
                'first_name',
                'last_name',
                'role',
            ]
