import datetime

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

from .models import Test, Students, AuthUser, Resume


# Create your views here.
# request.session.flush() или response.delete_cookie('sessionid') или logout(request) для завершения сессии пользователя
def home(request):
    if request.user.is_authenticated:
        # template = loader.get_template('home.html')
        # context = {}
        # return HttpResponse(template.render(context, request))
        resumeList = Resume.objects.all() #filter(id_student='1') # 1 нужно заменить на ИД студента!!! и убрать ".all()"
        return render(request, 'home.html', {'resume': resumeList})
    else:
        return redirect('login')

def myresume(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            student_form = StudentForm(request.POST)
            resume_form = ResumeForm(request.POST)
            education_form = EducationForm(request.POST)
            about_job_form = AboutJobForm(request.POST)
            if student_form.is_valid() and resume_form.is_valid():
                print(student_form.cleaned_data)
                print(resume_form.cleaned_data)
                user_id = request.user.id
                user = AuthUser.objects.get(pk=user_id)
                new_student_id = Students.objects.all().count()+1
                student = Students(id_student=new_student_id, surname=student_form.cleaned_data.get('surname'), name=student_form.cleaned_data.get('name'), middle_name=student_form.cleaned_data.get('middle_name'), birthdate=student_form.cleaned_data.get('birthday'),
                                    gender=dict(GENDER_CHOICES).get(student_form.cleaned_data.get('gender')), phone=student_form.cleaned_data.get('phone'), email=student_form.cleaned_data.get('email'),
                                    types_of_communication=dict(TYPES_OF_COMMUNICATION_CHOICES).get(student_form.cleaned_data.get('types_of_communication')), education_level=dict(EDUCATION_LEVEL_CHOICES).get(student_form.cleaned_data.get('education_level')), id_auth_user=user)
                new_resume_id=Resume.objects.all().count()+1
                resume = Resume(id_resume=new_resume_id, id_student=student, description_skills=resume_form.cleaned_data.get('description_skills'), city=resume_form.cleaned_data.get('city'), station_metro=resume_form.cleaned_data.get('station_metro'),
                                possibility_of_transfer=dict(POSSIBILITY_OF_TRANSFER_CHOICES).get(resume_form.cleaned_data.get('possibility_of_transfer')), business_trips=dict(BUSINESS_TRIPS_CHOICES).get(resume_form.cleaned_data.get('business_trips')),
                                desired_time_in_the_way=dict(DESIRED_TIME_CHOICES).get(resume_form.cleaned_data.get('desired_time_in_the_way')), availability_car=resume_form.cleaned_data.get('availability_car'), locale_resume=resume_form.cleaned_data.get('locale_resume'),
                                date_of_creation=datetime.datetime.now())
                with transaction.atomic():
                    student.save()
                    resume.save()
                    return redirect('home')
        else:
            student_form = StudentForm()
            resume_form = ResumeForm()
            education_form = EducationForm()
            about_job_form = AboutJobForm()
        return render(request, 'resume.html', {'student_form': student_form, 'resume_form': resume_form, 'education_form': education_form, 'about_job_form' : about_job_form})
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
