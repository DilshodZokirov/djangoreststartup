from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import UserMove, User


class UserMoveSerializer(ModelSerializer):
    lon = serializers.CharField(max_length=400)
    lot = serializers.CharField(max_length=400)

    class Meta:
        model = UserMove
        fields = [
            "lon",
            "lot",
            "user"
        ]

    def create(self, validated_data: dict):
        validated_data['user'] = self.context['request'].user
        user = UserMove(**validated_data)
        user.save()
        return "success"


class RequestUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number"
        ]


class UserMoveListSerializer(ModelSerializer):
    class Meta:
        model = UserMove
        fields = [
            "lon",
            "lot",
            "user"
        ]
