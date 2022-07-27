from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role == 'admin' or user.is_staff:
            return True
        return False
