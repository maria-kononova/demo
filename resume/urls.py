from django.urls import path

from resume import views


urlpatterns = [
    path("resume/home", views.home, name="home"),
    path("resume/myresume", views.myresume, name="myresume"),
    path("resume/", views.login_view, name="login"),
    path('resume/register', views.register_view, name='register'),
    path('resume/exit', views.exit, name='exit'),
    path('resume/<int:pk>/sample', views.go_to_sample, name='go_to_sample'),
    path("resume/account", views.account, name="account"),
    path("resume/edit", views.account_edit, name='account_edit')
]