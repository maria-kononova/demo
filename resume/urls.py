from django.urls import path

from resume import views


urlpatterns = [
    path("resume/", views.home, name="home"),
    path("resume/myresume", views.myresume, name="myresume")
]