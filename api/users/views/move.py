from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.serializers.move import UserMoveSerializer, UserMoveListSerializer
from apps.users.models import UserMove


class UserMoveApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserMoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "uz": "Joylashuv aniqlandi !!!",
                "en": "The location has been determined !!!",
                "ru": "Место было определено !!!"
            }
        )

    def get(self, request):
        queryset = UserMove.objects.filter(user=request.user, created_date__day=datetime.day)
        serializer = UserMoveListSerializer(queryset, many=True)
        return Response(serializer.data)
