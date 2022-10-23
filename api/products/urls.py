from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.products.views.agent import ProductModelViewSet

router = DefaultRouter()
router.register("", ProductModelViewSet)
urlpatterns = [
    path("", include(router.urls))

]
