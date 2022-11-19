from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.move import UserMoveModelView
# from .views.move import UserMoveApiView, UserGetMoveDetail
from .views.registration_views import RegistrationModelViewSet
from .views.member import WorkerModelViewSet

router = DefaultRouter()
router.register("move", UserMoveModelView)
urlpatterns = [
    path("", include(router.urls)),
]
