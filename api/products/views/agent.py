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
    queryset = Product.objects.all()
    serializer_class = AgentProductSerializer
    parser_classes = (MultiPartParser, FileUploadParser)
    filter_backends = (SearchFilter,)

    def list(self, request, *args, **kwargs):
        self.queryset = Product.objects.filter(company=request.user.company)
        return super(ProductModelViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = UpdateProductClassSerializer
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": {
                "uz": "Muoffaqiyatli o'zgartirildi",
                "en": "Successfully Updated",
                "ru": "Изменено успешно"
            }})

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = DetailProductSerializer
        return super(ProductModelViewSet, self).retrieve(request, *args, **kwargs)

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
                }}

        )
