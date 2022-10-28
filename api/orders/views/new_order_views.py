from django.http import Http404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.orders.serializers.new_order_serializer import OrderClassesSerializer, \
    CreateOrderProductSerializer, UpdateOrderProductSerializer, GetOneOrderSerializer, CreateOrderSerializer, \
    UpdateOrderSerializer
from apps.orders.models import Order, OrderProduct


class OrderProductViews(APIView):
    def post(self, request):
        serializer = CreateOrderProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "uz": "Maxsulot muoffaqiyatli qo'shildi !!!",
                "en": "Product added successfully !!!",
                "ru": "Продукт успешно добавлен !!!"
            }
        )


class OrderProductUpdateApiView(APIView):
    def get_object(self, pk):
        try:
            return OrderProduct.objects.get(pk=pk)
        except OrderProduct.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        order_product = self.get_object(pk=pk)
        serializer = UpdateOrderProductSerializer(order_product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "uz": "Muoffaqiyatli O'zgartirildi !!",
            "en": "Changed Successfully !!",
            "ru": "Изменено успешно !!",
        })


class OrderClientModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderClassesSerializer
    queryset = Order.objects.filter(is_deleted=False)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = GetOneOrderSerializer
        return super(OrderClientModelViewSet, self).retrieve(request, *args, **kwargs)

    @action(methods=['post'], detail=False)
    def create_order(self, request, *args, **kwargs):
        self.serializer_class = CreateOrderSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "uz": "Muvaffaqiyatli yaratildi !!!",
                "en": "Successfully Created !!!",
                "ru": "Создано успешно !!!"
            }
        )

    def destroy(self, request, *args, **kwargs):
        return super(OrderClientModelViewSet, self).destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = UpdateOrderSerializer
        return super(OrderClientModelViewSet, self).update(request, *args, **kwargs)
