from django.contrib.sites import requests
from rest_framework import serializers

from resume.models import AuthUser, Students, Resume


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = "__all__"


class StudentsSerializer(serializers.ModelSerializer):
    id_student = serializers.HiddenField(default=0)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Students
        fields = ("id_student", "surname", "name", "middle_name", "birthdate", "gender", "phone", "email", "user")


class ResumesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("moderation_status",)

# class StudentsSerializer(serializers.Serializer):
#     surname = serializers.CharField(max_length=30)
#     name = serializers.CharField(max_length=30)
#     middle_name = serializers.CharField(max_length=30, default=None)
#     birthdate = serializers.DateField()
#     gender = serializers.CharField(max_length=7)
#     #photo = serializers.TextField(db_column='Photo', blank=True, null=True)
#     phone = serializers.CharField(max_length=12)
#     email = serializers.CharField(max_length=45)
#     types_of_communication = serializers.CharField(max_length=45, default=None)
#     education_level = serializers.CharField(max_length=45, default=None)
#     id_auth_user = serializers.IntegerField()
#
#     def create(self, validated_data):
#         return Students.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.surname = validated_data.get("surname", instance.surname)
#         instance.name = validated_data.get("name", instance.name)
#         instance.middle_name = validated_data.get("middle_name", instance.middle_name)
#         instance.birthdate = validated_data.get("birthdate", instance.birthdate)
#         instance.gender = validated_data.get("gender", instance.gender)
#         instance.phone = validated_data.get("phone", instance.phone)
#         instance.email = validated_data.get("email", instance.email)
#         instance.types_of_communication = validated_data.get("types_of_communication", instance.types_of_communication)
#         instance.education_level = validated_data.get("education_level", instance.education_level)
#         instance.id_auth_user = validated_data.get("id_auth_user", instance.id_auth_user)
#         instance.save()
#         return instance
