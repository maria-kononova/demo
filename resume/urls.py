from django.urls import path, include, re_path
from rest_framework import routers

from resume import views
from resume.api import *

# router = routers.SimpleRouter()
# router.register(r'students', StudentsViewSet)
# #router.register(r'resume/api/auth_user', UserAPIView)

urlpatterns = [
    path("resume/home", views.home, name="home"),
    path("resume/myresume", views.myresume, name="myresume"),
    path("resume/", views.login_view, name="login"),
    path('resume/register', views.register_view, name='register'),
    path('resume/exit', views.exit, name='exit'),
    path('resume/sample', views.go_to_sample, name='go_to_sample'),
    path('resume/api/v1/drf-auth/', include('rest_framework.urls')),
    path('resume/api/v1/auth/', include('djoser.urls')),
    re_path(r'^resume/api/v1/auth/', include('djoser.urls.authtoken')),
    path('resume/api/v1/students/', StudentsAPIViewID.as_view()),
    path('resume/api/v1/students/create/', StudentsAPICreate.as_view()),
    path('resume/api/v1/students/<int:pk>/', StudentsAPIView.as_view()),
    path('resume/api/v1/students/update/<int:pk>/', StudentsAPIUpdate.as_view()),
    path('resume/api/v1/students/delete/<int:pk>/', StudentsAPIDelete.as_view()),
    path('resume/api/v1/resumes/<int:pk>/', ResumesAPIView.as_view()),
]
