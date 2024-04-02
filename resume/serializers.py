

from django.contrib.auth import password_validation
from django.contrib.sites import requests
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from resume.models import AuthUser, Students, Resume, Photo

""" Классы сериализации (из БД в JSON) данных"""

# Сериализация данных резюме (статус)
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ("id", "username")


# Сериализация данных студента
class StudentsSerializer(serializers.ModelSerializer):
    id_student = serializers.HiddenField(default=0)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Students
        fields = ("id_student", "surname", "name", "middle_name", "birthdate", "gender", "phone", "email", "user")


# Сериализация данных резюме (статус)
class ResumesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("moderation_status",)


# Сериализатор для сохранения фотографий
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

# Сериализатор для изменения пароля
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Старый пароль не правильный')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("Пароли не совпадают")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user