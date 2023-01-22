from datetime import datetime

from django.http.response import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.move import UserMoveSerializer, RequestUserSerializer, UserMoveUserSerializer
from apps.users.models import UserMove, User


class UserMoveModelView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]
    serializer_class = UserMoveSerializer
    queryset = UserMove.objects.filter(is_deleted=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer['user'] = request.user
        serializer.save()
        return Response(
            {
                "message": {
                    "uz": "Joylashuv aniqlandi",
                    "уз": "Жойлашув аниқланди",
                    "ru": "Место было определено"
                }}
        )


class UserMoveDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserMoveUserSerializer(snippet)
        return Response(serializer.data)
