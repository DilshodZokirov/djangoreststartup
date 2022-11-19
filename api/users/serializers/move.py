import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import UserMove, User, District


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
        validated_data["user"] = self.context['request'].user
        user = UserMove(**validated_data)
        user.save()
        return user


class RequestUserSerializer(ModelSerializer):
    # user_move = UserMoveListSerializer(many=True)

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
            "created_date",
        ]


class DistrictUserSerializer(ModelSerializer):
    class Meta:
        model = District
        fields = [
            "id",
            "name",
        ]


class UserMoveUserSerializer(ModelSerializer):
    user_move = UserMoveListSerializer(many=True)
    district = DistrictUserSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "district",
            "phone_number",
            "user_move"
        ]
# class UserMoveListSerializer(ModelSerializer):
#     user = RequestUserSerializer()
#
#     class Meta:
#         model = UserMove
#         fields = [
#             "id",
#             "lon",
#             "lot",
#             'user',
#             "created_date",
#         ]
