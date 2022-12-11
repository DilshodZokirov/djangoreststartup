from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.users.serializers.registration import LoginUserSerializer, RegistrationSerializer, UserCheckChatIdSerializer
from apps.users.models import User


class RegistrationModelViewSet(ModelViewSet):
    parser_classes = [JSONParser, ]
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()

    @swagger_auto_schema(method='post', request_body=LoginUserSerializer)
    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = LoginUserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.validated_data['token']
        role = user.role
        return Response({
            'user_id': user.pk,
            'token': token.key,
            'role_id': role if role else None
        })

    @swagger_auto_schema(method='post', request_body=RegistrationSerializer)
    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": {
                "uz": "Muvaffaqiyatli ro'yxatdan o'tdingiz",
                "уз": "Муваффақиятли рўйхатдан ўтдингиз",
                "ru": "Вы успешно зарегистрированы",
            }})

    @action(methods=["PUT"], detail=False)
    def chat_id_update(self, request, *args, **kwargs):
        self.serializer_class = UserCheckChatIdSerializer
        if User.objects.get(chat_id__isnull=True):
            serializer = self.get_serializer(self.get_object(), data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(request)
            return Response("Muvaffaqiyatli o'zgartirildi")
        return Response("Bunaqa o'zgaruvchi bor")
