from datetime import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.serializers.move import UserMoveSerializer, UserMoveListSerializer, RequestUserSerializer
from apps.users.models import UserMove, User


class UserMoveApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = UserMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": {
                    "uz": "Joylashuv aniqlandi",
                    "en": "The location has been determined",
                    "ru": "Место было определено"
                }}
        )


class UserGetMoveDetail(APIView):
    def get(self, request, pk=None):
        queryset = UserMove.objects.filter(user=pk, created_date__day=datetime.day)
        serializer = UserMoveListSerializer(queryset, many=True)
        return Response(serializer.data)
