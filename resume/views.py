import datetime
from django.forms import formset_factory
from django.db import transaction
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

from .dictionary import GENDER_CHOICES, TYPES_OF_COMMUNICATION_CHOICES, EDUCATION_LEVEL_CHOICES, \
    POSSIBILITY_OF_TRANSFER_CHOICES, BUSINESS_TRIPS_CHOICES, DESIRED_TIME_CHOICES
from .forms import UserLoginForm, StudentForm, ResumeForm, EducationForm, AboutJobForm
from .forms import UserRegistrationForm
import json

from .models import Test, Students, AuthUser, Resume, EducationalInstitution
from .create_object import create_student, create_resume, create_education, create_about_job, create_specialization, \
    create_busyness, create_work_timetable


# Create your views here.
# request.session.flush() или response.delete_cookie('sessionid') или logout(request) для завершения сессии пользователя
def home(request):
    if request.user.is_authenticated:
        # template = loader.get_template('home.html')
        # context = {}
        # return HttpResponse(template.render(context, request))
        user_id = request.user.id
        user = AuthUser.objects.get(pk=user_id)
        student = Students.objects.filter(id_auth_user=user)
        resumeList = []
        if student.count() != 0:
            resumeList = Resume.objects.filter(id_student=student[0])  # filter(id_student='1') # 1 нужно заменить на ИД студента!!! и убрать ".all()"
        return render(request, 'home.html', {'resume': resumeList})
    else:
        return redirect('login')


def myresume(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(list(request.POST.items()))
            student_form = StudentForm(request.POST)
            resume_form = ResumeForm(request.POST)
            education_form = EducationForm(request.POST)
            about_job_form = AboutJobForm(request.POST)
            if student_form.is_valid() and resume_form.is_valid() and education_form.is_valid() and about_job_form.is_valid():
                print(student_form.cleaned_data)
                print(resume_form.cleaned_data)
                print(education_form.cleaned_data)
                print(about_job_form.cleaned_data)
                user_id = request.user.id
                user = AuthUser.objects.get(pk=user_id)
                student = create_student(student_form, user)
                resume = create_resume(resume_form, student)
                education = create_education(education_form, resume)
                about_job = create_about_job(about_job_form, resume)
                specialization = create_specialization(about_job_form, about_job)
                busyness = create_busyness(about_job_form, about_job)
                work_timetable = create_work_timetable(about_job_form, about_job)
                with transaction.atomic():
                    student.save()
                    resume.save()
                    education.save()
                    about_job.save()
                    specialization.save()
                    busyness.save()
                    work_timetable.save()
                    return redirect('home')
        else:
            return render(request, 'resume.html', {'student_form': StudentForm(), 'resume_form': ResumeForm(),
                                                   'education_form': EducationForm(), 'about_job_form': AboutJobForm()})
        # template = loader.get_template('resume.html')
        # context = {}  # 'student': Students.objects.all().first()
        # return HttpResponse(template.render(context, request))
    else:
        return redirect('login')


def login_view(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('home')


def register_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')  # Перенаправление на страницу входа после успешной регистрации
        else:
            form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})
    else:
        return redirect('home')

def exit(request):
    request.session.flush()
    return redirect('login')
