from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.users.serializers.member import UserCreateSerializer, GetAllSerializer
from apps.users.models import User
from distributive.permissions import IsDirector


class WorkerModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = User.objects.filter(~Q(role='unemployed'))
    parser_classes = [MultiPartParser, FileUploadParser]
    serializer_class = GetAllSerializer
    filter_backends = (SearchFilter,)

    # @action(methods=["post"], detail=False)
    # def create_district(self, request):
    #     self.serializer_class =

    # @swagger_auto_schema(method="post", request_body=UserCreateSerializer,
    #                      responses={200: "Successfully Created", 400: "Bad Request"})
    @action(methods=["post"], detail=False)
    def create_worker(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Successfully Created"}
        )
