from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.orders.serializers.new_order_serializer import OrderClassesSerializer, \
    CreateOrderProductSerializer, UpdateOrderProductSerializer, GetOneOrderSerializer, CreateOrderSerializer, \
    UpdateOrderSerializer, DetailOrderSerializer, NewOrderCreateSerializer
from apps.orders.models import Order, OrderProduct


# class OrderProductViews(APIView):
#     def post(self, request):
#         serializer = CreateOrderProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {
#                 "uz": "Maxsulot muoffaqiyatli qo'shildi",
#                 "en": "Product added successfully ",
#                 "ru": "Продукт успешно добавлен "
#             }
#         )
#
#
# class OrderProductUpdateApiView(APIView):
#     def get_object(self, pk):
#         try:
#             return OrderProduct.objects.get(pk=pk)
#         except OrderProduct.DoesNotExist:
#             raise Http404
#
#     def put(self, request, pk, format=None):
#         order_product = self.get_object(pk=pk)
#         serializer = UpdateOrderProductSerializer(order_product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({
#             "uz": "Muoffaqiyatli O'zgartirildi",
#             "en": "Changed Successfully",
#             "ru": "Изменено успешно",
#         })


class OrderClientModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NewOrderCreateSerializer
    queryset = Order.objects.filter(is_deleted=False)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = GetOneOrderSerializer
        return super(OrderClientModelViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": {
            "uz": "Muoffaqiyatli O'zgartirildi",
            "en": "Successfully Updated",
            "ru": "Создано успешно"
        }})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": {
                "uz": "Muvaffaqiyatli yaratildi",
                "en": "Successfully Created",
                "ru": "Изменено успешно"
            }}
        )
