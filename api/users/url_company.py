from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.company_views import CompanyApiViewModel
from .views.move import UserMoveModelView, UserMoveDetail
# from .views.move import UserMoveApiView, UserGetMoveDetail
from .views.registration_views import RegistrationModelViewSet
from .views.member import WorkerModelViewSet

router = DefaultRouter()
router.register("company", CompanyApiViewModel)
urlpatterns = [
    path("", include(router.urls)),
]
