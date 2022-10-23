from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.products.serializers.agent_serializer import AgentProductSerializer
from apps.product.models import Product


class ProductModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Product.objects.all().order_by('-id')
    serializer_class = AgentProductSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    filter_backends = (SearchFilter,)
