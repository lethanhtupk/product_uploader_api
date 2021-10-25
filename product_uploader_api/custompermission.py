from rest_framework import permissions


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user


class IsAdminOrAssigneeReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.users.all() or request.user.is_staff == True
        else:
            return request.user.is_staff == True


# class IsAdminOrRequestOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user.profile or request.user.profile.role == 3


# class IsAdminOrProfileOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.user == request.user or request.user.profile.role == 3


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_staff == True
