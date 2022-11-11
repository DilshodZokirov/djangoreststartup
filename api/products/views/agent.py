from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.products.serializers.agent_serializer import AgentProductSerializer, ProductCreateSerializer, \
    DetailProductSerializer, UpdateProductClassSerializer
from apps.product.models import Product


class ProductModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Product.objects.all().order_by('-id')
    serializer_class = AgentProductSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    filter_backends = (SearchFilter,)

    @action(methods=['post'], detail=False)
    def create_product(self, request):
        self.serializer_class = ProductCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": {
                    "uz": "Muvaffaqiyatli yaratildi",
                    "en": "Successfully Created",
                    "ru": "Создано успешно"
                }
            }
        )

    def list(self, request, *args, **kwargs):
        self.queryset = Product.objects.filter(temporarily_unavailable=True)
        return super(ProductModelViewSet, self).list(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = UpdateProductClassSerializer
        return super(ProductModelViewSet, self).partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = DetailProductSerializer
        return super(ProductModelViewSet, self).retrieve(request, *args, **kwargs)
