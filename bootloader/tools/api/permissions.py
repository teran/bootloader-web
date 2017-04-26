from rest_framework.permissions import BasePermission, SAFE_METHODS


class StaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or \
            request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or \
            request.method in SAFE_METHODS
