import datetime
from django.forms import formset_factory
from django.db import transaction
from django.shortcuts import render, get_object_or_404
import requests
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
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
        user_id = request.user.id
        user = AuthUser.objects.get(pk=user_id)
        student = Students.objects.filter(id_auth_user=user)
        resumeList = []
        if user.is_staff:  # Проверяем, является ли пользователь модератором
            resumeList = Resume.objects.filter(moderation_status='модерация')
        else:
            if student.count() != 0:
                resumeList = Resume.objects.filter(id_student=student[0])
        return render(request, 'home.html', {'resume': resumeList})
    else:
        return redirect('login')


def myresume(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            resume_form = ResumeForm(request.POST)
            education_form = EducationForm(request.POST)
            about_job_form = AboutJobForm(request.POST)
            if resume_form.is_valid() and education_form.is_valid() and about_job_form.is_valid():
                user_id = request.user.id
                user = AuthUser.objects.get(pk=user_id)
                student_ = Students.objects.filter(id_auth_user=user)
                student = student_[0]
                resume = create_resume(resume_form, student)
                education = create_education(education_form, resume)
                about_job = create_about_job(about_job_form, resume)
                specialization = create_specialization(about_job_form, about_job)
                busyness = create_busyness(about_job_form, about_job)
                work_timetable = create_work_timetable(about_job_form, about_job)
                with transaction.atomic():
                    resume.save()
                    education.save()
                    about_job.save()
                    specialization.save()
                    busyness.save()
                    work_timetable.save()
                    return redirect('home')
        else:
            return render(request, 'resume.html', {'resume_form': ResumeForm(),
                                                   'education_form': EducationForm(), 'about_job_form': AboutJobForm()})
    else:
        return redirect('login')


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            login_data = request.POST.dict()
            username = login_data.get("username")
            password = login_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff == 1:  # Если is_staff равно 1, то пользователь - модератор
                    user_type = 'Модератор'
                else:
                    user_type = 'Студент'
                request.session['user_type'] = user_type
                return render(request, 'home.html', {
                    'user_type': user_type})  # Перенаправление на страницу "home" с передачей типа пользователя в контексте
            else:
                form = UserLoginForm()
                return render(request, 'login.html', {'form': form, 'msg': "Пароль или имя пользователя неверное"})
        else:
            form = UserLoginForm()
        return render(request, 'login.html', {'form': form, 'msg': ""})
    else:
        user_type = 'Модератор' if request.user.is_staff == 1 else 'Студент'
        return render(request, 'home.html', {'user_type': user_type})


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


def go_to_sample(request):
    return render(request, 'sample.html')


def account(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Сохранение данных пользователя
            print(list(request.POST.items()))
            student_form = StudentForm(request.POST)
            if student_form.is_valid():
                print(student_form.cleaned_data)
                user_id = request.user.id
                user = AuthUser.objects.get(pk=user_id)
                student_ = Students.objects.filter(id_auth_user=user)
                if student_.count() != 0:
                    student = student_[0]
                else:
                    student = create_student(student_form, user)
                with transaction.atomic():
                    student.save()
                    return redirect('account')
        else:
            # Вывод данных пользователя
            update_check = 0
            user_id = request.user.id
            user = AuthUser.objects.get(pk=user_id)
            studentList = Students.objects.filter(id_auth_user=user)
            return render(request, 'account.html',
                          {'student': studentList, 'student_form_account': StudentForm(), 'update_check': update_check})
    else:
        return redirect('login')


def account_edit(request):
    if request.user.is_authenticated:
        # student = get_object_or_404(Students, pk=pk)
        user_id = request.user.id
        user = AuthUser.objects.get(pk=user_id)
        update_check = 1
        if request.method == "POST":
            if 'edit_btn' in request.POST:
                # Сохранение измененных данных
                # form = StudentForm(request.POST, instance=student)
                student_form = StudentForm(request.POST)
                if student_form.is_valid():
                    student_ = Students.objects.filter(id_auth_user=user)
                    student = student_[0]
                    student.surname = request.POST['surname']
                    student.name = request.POST['name']
                    student.middle_name = request.POST['middle_name']
                    # С датой проблемки ((
                    # student.birthdate = student_form.cleaned_data['birthday']
                    # student.birthdate = request.POST['birthday_year'] + "-" + request.POST['birthday_month'] + "-" + request.POST['birthday_day']
                    student.gender = request.POST['gender']
                    student.phone = request.POST['phone']
                    student.email = request.POST['email']
                    student.types_of_communication = request.POST['types_of_communication']
                    student.education_level = request.POST['education_level']
                    with transaction.atomic():
                        # Добавьте 'birthday'
                        student.save(update_fields=['surname', 'name', 'middle_name', 'gender', 'phone', 'email',
                                                    'types_of_communication', 'education_level'])
                        return redirect('account')
        else:
            # Вывод формы для изменения данных (сами данные из бд пока не выгружаются для редактирования)
            # form = StudentForm(instance=student)
            studentList = Students.objects.filter(id_auth_user=user)
            return render(request, 'account.html',
                          {'student': studentList, 'student_form_account': StudentForm(), 'update_check': update_check})
    else:
        return redirect('login')
