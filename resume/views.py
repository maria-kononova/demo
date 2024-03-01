from django.shortcuts import render
import requests
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .dictionary import GENDER_CHOICES, TYPES_OF_COMMUNICATION_CHOICES, EDUCATION_LEVEL_CHOICES
from .forms import UserLoginForm, ResumeForm
from .forms import UserRegistrationForm
import json

from .models import Test, Students


# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def myresume(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            students = Students(surname=form.cleaned_data.get('surname'), name=form.cleaned_data.get('name'), middle_name=form.cleaned_data.get('middle_name'), birthdate=form.cleaned_data.get('birthday'),
                                gender=GENDER_CHOICES[int(form.cleaned_data.get('gender'))-1][1], phone=form.cleaned_data.get('phone'), email=form.cleaned_data.get('email'),
                                types_of_communication=TYPES_OF_COMMUNICATION_CHOICES[int(form.cleaned_data.get('types_of_communication'))-1][1], education_level=EDUCATION_LEVEL_CHOICES[int(form.cleaned_data.get('education_level'))-1][1])
            students.save()
    else:
        form = ResumeForm()

    return render(request, 'resume.html', {'form': form})
    # template = loader.get_template('resume.html')
    # context = {}  # 'student': Students.objects.all().first()
    # return HttpResponse(template.render(context, request))


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        login_data = request.POST.dict()
        username = login_data.get("username")
        password = login_data.get("password")
        print(username, password)
        # user = auth(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после успешной авторизации
        else:
            form = UserLoginForm()
            return render(request, 'login.html', {'form': form, 'msg': "Пароль или имя пользователя неверное"})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form, 'msg': ""})


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# def auth(username, password):
#     for user in User.objects.all():
#         if user.login == username and user.password == password:
#             print("ok")
#             return user
