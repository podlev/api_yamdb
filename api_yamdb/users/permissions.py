from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.role == 'admin':
            return True
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS or (request.user.is_authenticated and user.role == 'admin'):
            return True
        return False


class IsModerator(BasePermission):
    pass
