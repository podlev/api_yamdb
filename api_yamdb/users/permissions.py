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
        if (request.method in SAFE_METHODS or
                (request.user.is_authenticated and user.role == 'admin')):
            return True
        return False


class IsModerator(BasePermission):
    """Права доступа администратор, модератор, автор или только для чтения"""

    def has_permission(self, request, view):
        user = request.user
        if (request.method in SAFE_METHODS or
                (request.user.is_authenticated and user.role == 'admin') or
                (request.method == "PATCH" and
                 request.user.role == 'moderator')):
            return True
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS or (request.user.is_authenticated and (user.role == 'admin' or user.is_staff)):
            return True
        return False


class IsModerator(BasePermission):
    pass