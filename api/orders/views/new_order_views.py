from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.orders.serializers.new_order_serializer import OrderClassesSerializer


class OrderClientModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderClassesSerializer
