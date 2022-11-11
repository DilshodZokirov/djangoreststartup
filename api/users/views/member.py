from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api.users.serializers.member import UserCreateSerializer, GetAllSerializer, DistrictClassMemberSerializer, \
    MemberAllSerializer, DetailUserCompanySerializer, MemberUpdateSerializer
from apps.users.models import User, District, Company
from distributive.permissions import IsDirector


class WorkerModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = User.objects.filter(~Q(role='unemployed'))
    parser_classes = [MultiPartParser, FileUploadParser]
    serializer_class = GetAllSerializer
    filter_backends = (SearchFilter,)

    @action(methods=["post"], detail=False)
    def create_worker(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Successfully Created"}
        )

    def list(self, request, *args, **kwargs):
        self.queryset = User.objects.filter(company=request.user.company)
        self.serializer_class = MemberAllSerializer
        return super(WorkerModelViewSet, self).list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = MemberUpdateSerializer
        return super(WorkerModelViewSet, self).put(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = DetailUserCompanySerializer
        return super(WorkerModelViewSet, self).retrieve(request, *args, **kwargs)


class DistrictApiView(APIView):
    def get(self, request, format=None):
        queryset = District.objects.all()
        serializer = DistrictClassMemberSerializer(queryset, many=True)
        return Response(serializer.data)
