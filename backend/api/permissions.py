from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''Разрешение создания, изменения и удаления только автору или админу.'''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            obj.author == request.user
            or request.user.is_staff)
