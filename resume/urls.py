from django.urls import path, include, re_path
from resume import views
from resume.api import *
from resume.views import get_image

urlpatterns = [
    # Переходы приложения
    path("resume/home", views.home, name="home"),
    path("resume/myresume", views.myresume, name="myresume"),
    path("resume/", views.login_view, name="auth"),
    path('resume/register', views.register_view, name='register'),
    path('resume/exit', views.exit, name='exit'),
    path('resume/<int:pk>/sample', views.go_to_sample, name='go_to_sample'),
    path('resume/<int:pk>/edit', views.resume_edit, name='resume_edit'),
    path("resume/account", views.account, name="account"),
    path('resume/sample', views.go_to_sample, name='go_to_sample'),
    path('resume/upload', views.upload_image, name="upload"),
    path('resume/auth_hh/<str:pk>', views.auth_hh, name='auth_hh'),
    path('resume/send/<int:pk>/', views.resume_send),
    path('resume/access/<int:pk>/', views.get_access_token_view),
    path('get_data/', views.get_data, name='get_data'),
    # Конечные точки API
    path('resume/api/v1/drf-auth/', include('rest_framework.urls')),
    path('resume/api/v1/auth/', include('djoser.urls')),
    re_path(r'^resume/api/v1/auth/', include('djoser.urls.authtoken')),
    path('resume/api/v1/students/', StudentsAPIViewID.as_view()),
    path('resume/api/v1/students/create/', StudentsAPICreate.as_view()),
    path('resume/api/v1/students/<int:pk>/', StudentsAPIView.as_view()),
    path('resume/api/v1/students/update/<int:pk>/', StudentsAPIUpdate.as_view()),
    path('resume/api/v1/students/delete/<int:pk>/', StudentsAPIDelete.as_view()),
    path('resume/api/v1/resumes/', ResumesIDAPIView.as_view()),
    path('resume/api/v1/resumes/<int:pk>/', ResumesAPIView.as_view()),
    path('resume/api/v1/users/update/username/', UsersAPIUpdate.as_view()),
    path('resume/api/v1/users/update/password/', ChangePasswordView.as_view()),
    path('resume/api/v1/upload/', PhotoUploadView.as_view(), name='photo-upload'),
    path('get-image/<str:image_name>/', get_image, name='get_image'),
]
