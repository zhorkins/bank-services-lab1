from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Разрешение только для модераторов (пользователей с is_moderator=True).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_moderator

class IsOwnerOrModerator(permissions.BasePermission):
    """
    Разрешение, позволяющее доступ владельцу объекта или модератору.
    """
    def has_object_permission(self, request, view, obj):
        # Модератор может всё
        if request.user.is_moderator:
            return True
        # Если есть поле created_by (операционист), проверяем, что текущий пользователь – его владелец
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False