from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsEmployee(BasePermission):
    message = 'Only employees can perform this action.'

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and hasattr(user, 'employee'))
