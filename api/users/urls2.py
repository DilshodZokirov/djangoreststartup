from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.registration_views import RegistrationModelViewSet
from .views.member import WorkerModelViewSet

router = DefaultRouter()
router.register("worker", WorkerModelViewSet)

urlpatterns = [
    path("", include(router.urls))
]
