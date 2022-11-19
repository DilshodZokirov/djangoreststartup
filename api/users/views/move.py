from datetime import datetime

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.move import UserMoveSerializer, UserMoveListSerializer, RequestUserSerializer
from apps.users.models import UserMove, User


class UserMoveModelView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]
    serializer_class = UserMoveSerializer
    queryset = UserMove.objects.filter(is_deleted=False)

    def create(self, request, *args, **kwargs):
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

    def retrieve(self, request, *args, **kwargs):
        queryset = UserMove.objects.filter(user=kwargs['pk'], created_date__day=datetime.day)
        self.serializer_class = UserMoveSerializer
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

