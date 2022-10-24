from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.orders.views.new_order_views import OrderClientModelViewSet, OrderProductViews, OrderProductUpdateApiView

router = DefaultRouter('agent_order', OrderClientModelViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path('order_product/', OrderProductViews.as_view()),
    path('order_product/<pk>/', OrderProductUpdateApiView.as_view()),

]
