from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'


class IsUserRole(permissions.BasePermission):
    """
    Permission to only allow regular users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'USER'


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to allow admin users full access and read-only access to others.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'
