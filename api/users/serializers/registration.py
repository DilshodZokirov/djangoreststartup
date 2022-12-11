from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from apps.users.models import User, Company


class UserCheckChatIdSerializer(serializers.ModelSerializer):
    chat_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'chat_id'
        ]


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
                raise serializers.ValidationError({
                    "message": {
                        "uz": "Bunaqa inson topilmadi",
                        "ru": "Пользователь не найден",
                        "уз": 'Бунақа инсон топилмади'
                    }
                })
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
    chat_id = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            'company',
            "phone_number",
            "password",
            "password2",
            "chat_id"
        ]
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}

    def validate(self, attrs: dict):
        phone_number = attrs.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(
                {"message": {
                    "uz": "Bunaqa telefon nomerli inson bizda bor iltimos boshqa nomerdan foydalaning yoki login qismiga o'ting",
                    "уз": "Бунақа телефон номерли инсон бизда бор илтимос бошқа номердан фойдаланинг ёки логин қисмига ўтинг",
                    "ru": "У нас есть человек с таким номером телефона, пожалуйста используйте другой номер или зайдите в раздел авторизации"
                }
                })
        if 10 >= len(phone_number) >= 12:
            raise ValidationError(
                {
                    "message": {
                        "uz": "Iltimos telefon nomerni to'g'ri kiriting",
                        "уз": "Илтимос телефон номерни тўғри киритинг",
                        "ru": "Пожалуйста, введите правильный номер телефона"
                    }})
        if attrs.get('password') != attrs.get("password2"):
            raise ValidationError(
                {
                    "message": {
                        "uz": "Iltimos parolni to'g'ri kiriting",
                        "уз": "Илтимос паролни тўғри киритинг",
                        "ru": "Пожалуйста, введите правильный пароль"
                    }
                })
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError(
                {
                    "message": {
                        "uz": "Bunaqa inson bizning ro'yxatda bor",
                        "уз": "Бунақа инсон бизнинг рўйхатда бор",
                        "ru": "Такой человек есть в нашем списке"
                    }
                })
        if Company.objects.filter(name=attrs.get("company")).exists():
            raise ValidationError(
                {
                    "message": {
                        "uz": "Bunday korxona bizda bor iltimos boshqa nom qo'ying ",
                        "уз": "Бундай корхона бизда бор илтимос бошқа ном қўйинг",
                        "ru": "У нас есть такая компания, дайте ей другое название"
                    }
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
        chat_id = validated_data.get('chat_id')
        company = Company.objects.create(name=company_name)
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number,
            company=company,
            role="office_manager",
            is_director=True,
            chat_id=chat_id
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
