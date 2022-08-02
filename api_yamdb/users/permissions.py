from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Права доступа администратор"""

    def has_permission(self, request, view):
        user = request.user
        if user.role == 'admin':
            return True
        return False


class IsAdminOrReadOnly(BasePermission):
    """Права доступа администратор или только для чтения"""

    def has_permission(self, request, view):
        user = request.user
        if (request.method in SAFE_METHODS
                or (request.user.is_authenticated and user.role == 'admin')):
            return True
        return False


class IsReadOnlyOrIsAuthorOrIsModerator(BasePermission):
    """Права доступа администратор, модератор, автор или только для чтения"""

    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS or user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            user.role == 'admin'
            or user.role == 'moderator'
            or obj.author == user)
