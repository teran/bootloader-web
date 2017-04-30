from rest_framework.permissions import BasePermission, SAFE_METHODS


class StaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or \
            (request.method in SAFE_METHODS and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or \
            (request.method in SAFE_METHODS and request.user.is_authenticated)


class OwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
            request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
