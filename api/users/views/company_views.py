from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.company import GetCompanyModelSerializer
from apps.users.models import Company


class CompanyApiViewModel(ModelViewSet):
    serializer_class = GetCompanyModelSerializer
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Company.objects.filter(is_delete=False)
    # parser_classes = [MultiPartParser, FileUploadParser]
    filter_backends = (SearchFilter,)

    def list(self, request, *args, **kwargs):
        self.serializer = GetCompanyModelSerializer
        return super(CompanyApiViewModel, self).list(request, *args, **kwargs)
