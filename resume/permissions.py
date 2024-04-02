from rest_framework import permissions

from resume.models import Students, AuthUser

""" Классы Permissions используются для определения прав доступа к тому или иному объекту  при образении к API"""

# Права доступа только администратору(обновление, удаление) или только чтение
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


# Права доступа только создателю(обновление, удаление) или только чтение
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


# Права доступа только создателю пользователю
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# Права доступа только создателю студенту
class IsOwnerStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        student = Students.objects.filter(user=request.user).first()
        return obj.id_student == student

