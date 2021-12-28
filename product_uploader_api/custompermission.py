from rest_framework import permissions
USER = 1
ADMIN = 2
SUPER_ADMIN = 3


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role in [ADMIN, SUPER_ADMIN])


class HasHigherPrivilege(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role > obj.role or request.user.role == SUPER_ADMIN or (request.user.role == ADMIN and request.user.id == obj.id)


class IsAdminOrAssigneeReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.users.all() or request.user.is_staff == True
        else:
            return request.user.role in [ADMIN, SUPER_ADMIN]


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.role in [ADMIN, SUPER_ADMIN]


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == SUPER_ADMIN
