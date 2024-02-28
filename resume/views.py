from django.shortcuts import render
import requests
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import AuthenticationForm

import json

from resume.models import Students, User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def myresume(request):
    template = loader.get_template('resume.html')
    context = {}  # 'student': Students.objects.all().first()
    return HttpResponse(template.render(context, request))


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        login_data = request.POST.dict()
        username = login_data.get("username")
        password = login_data.get("password")
        print(username, password)
        #user = auth(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после успешной авторизации
        else:
            form = UserLoginForm()
            return render(request, 'login.html', {'form': form, 'msg': "Пароль или имя пользователя неверное"})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form, 'msg' : ""})


def auth(username, password):
    for user in User.objects.all():
        if user.login == username and user.password == password:
            print("ok")
            return user
