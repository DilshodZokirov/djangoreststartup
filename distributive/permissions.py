from rest_framework.permissions import BasePermission


class IsDirector(BasePermission):
    message = "Siz Director emassiz shuning uchun bu ma'lumotlani kora olmaysiz !!!"
    def has_permission(self, request, view):
        return bool(request.user.role == "office_manager" and request.user.is_authenticated)
