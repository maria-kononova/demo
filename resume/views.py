import datetime
import os

from django.forms import formset_factory
from django.db import transaction
from django.shortcuts import render, get_object_or_404
import requests
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .api import get_token, post_request
from .dictionary import GENDER_CHOICES, TYPES_OF_COMMUNICATION_CHOICES, EDUCATION_LEVEL_CHOICES, \
    POSSIBILITY_OF_TRANSFER_CHOICES, BUSINESS_TRIPS_CHOICES, DESIRED_TIME_CHOICES
from .forms import UserLoginForm, StudentForm, ResumeForm, EducationForm, AboutJobForm, TestsExamsForm, CoursesForm
from .forms import UserRegistrationForm
import json

from .models import Test, Students, AuthUser, Resume, EducationalInstitution, AboutJob, Specialization, Busyness, \
    WorkTimetable, Photo
from .create_object import create_student, create_resume, create_education, create_about_job, create_specialization, \
    create_busyness, create_work_timetable, create_courses, create_tests_exams
from .serializers import StudentsSerializer


# Create your views here.
# request.session.flush() или response.delete_cookie('sessionid') или logout(request) для завершения сессии пользователя
def register_view(request):
    """ Функция, используемая для регистрации нового пользователя. """
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                request.session['student_created'] = 0
                return redirect('home')
        else:
            form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})
    else:
        return redirect('home')


def login_view(request):
    """ Функция, используемая для входа пользователя в систему. """
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
                request.session['resume_choice'] = 0
                student = Students.objects.filter(user=user)
                if student:
                    request.session['student_created'] = 1
                else:
                    request.session['student_created'] = 0
                return redirect('home')
            else:
                form = UserLoginForm()
                return render(request, 'login.html', {'form': form, 'msg': "Пароль или имя пользователя неверное"})
        else:
            form = UserLoginForm()
            return render(request, 'login.html', {'form': form, 'msg': ""})
    else:
        return redirect('home')


def exit(request):
    """ Функция, используемая для выхода пользователя из системы. """
    request.session.flush()
    return redirect('auth')


def home(request):
    """ Функция, используемая для отображения главной страницы. """
    if request.user.is_authenticated:
        user = request.user
        student = Students.objects.filter(user=user)
        resumeList = []
        if user.is_staff:  # Проверяем, является ли пользователь модератором
            resumeList = Resume.objects.filter(moderation_status='модерация')
        else:
            if student.count() != 0:
                resumeList = Resume.objects.filter(id_student=student[0])
        return render(request, 'home.html', {'resume': resumeList})
    else:
        return redirect('auth')


def account(request):
    """ Функция, используемая для отображения аккаунта студента (сохранение данных или вывод данных из базы). """
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Сохранение и изменение данных пользователя
            student_form = StudentForm(request.POST)
            if student_form.is_valid():
                if 'save_btn' in request.POST:
                    # Нажата кнопка для сохранения / изменения
                    user = request.user
                    student = Students.objects.filter(user=user).first()
                    if student:
                        # Обновление данных, т. к. студент есть
                        id_student = Students.objects.filter(user=user).first().id_student
                        student = create_student(student_form, user, id_student)
                        with transaction.atomic():
                            student.save(
                                update_fields=['surname', 'name', 'middle_name', 'birthdate', 'gender', 'phone',
                                               'email',
                                               'types_of_communication', 'education_level'])
                    else:
                        # Создание нового студента
                        student = create_student(student_form, user, None)
                        # token, created = Token.objects.get_or_create(user=user)
                        # post_request("resume/api/v1/students/create/", StudentsSerializer(student).data, token.key)
                        with transaction.atomic():
                            student.save()
                    request.session['student_created'] = 1
                    return redirect('account')
        else:
            # Если у пользователя не заполнены данные в аккаунте, попадаем на форму сохранения данных (без аватарки)
            # Если у пользователя заполнены данные в аккаунте и update_check = 0 - вывод данных студента
            # Если у пользователя заполнены данные в аккаунте и update_check = 1 - форма изменения данных (доступен выбор аватарки)
            user = request.user
            student = Students.objects.filter(user=user).first()
            update_check = 0
            student_form = StudentForm()
            if 'edit_btn' in request.GET:
                # Нажатие на кнопку "Изменить данные"
                update_check = 1
                # student_form = StudentForm(instance=student) # Так вроде должны подгружаться данные и бд, но тут ошибка
            photo_name = ""
            if student:
                if student.photo:
                    photo = Photo.objects.get(id=student.photo.id)
                    photo_name = ""
                    if photo:
                        photo_name = photo.image.name.split(sep='/')[1]
            return render(request, 'account.html',
                          {'student': student, 'student_form_account': student_form, 'update_check': update_check,
                           'photo': photo_name})  # 'photo': photo_name
    else:
        return redirect('auth')


def get_image(request, image_name):
    """ Функция, используемая для выгрузки фотографии студента. """
    folder_name = 'photo'
    path = os.path.join(os.getcwd(), folder_name, image_name)
    with open(path, 'rb') as image_file:
        return HttpResponse(image_file.read())


def myresume(request):
    """ Функция, используемая для отображения страницы "Создать резюме" и сохранения резюме. """
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Сохранение в БД
            resume_form = ResumeForm(request.POST)
            education_form = EducationForm(request.POST)
            courses_form = CoursesForm(request.POST)
            tests_exams_form = TestsExamsForm(request.POST)
            about_job_form = AboutJobForm(request.POST)
            if (resume_form.is_valid() and education_form.is_valid() and courses_form.is_valid()
                    and tests_exams_form.is_valid() and about_job_form.is_valid()):
                user = request.user
                student = Students.objects.filter(user=user).first()
                resume = create_resume(resume_form, student)
                education = create_education(education_form, resume)
                courses = create_courses(courses_form, resume)
                tests_exams = create_tests_exams(tests_exams_form, resume)
                about_job = create_about_job(about_job_form, resume)
                specialization = create_specialization(about_job_form, about_job)
                busyness = create_busyness(about_job_form, about_job)
                work_timetable = create_work_timetable(about_job_form, about_job)
                with transaction.atomic():
                    resume.save()
                    education.save()
                    courses.save()
                    tests_exams.save()
                    about_job.save()
                    specialization.save()
                    busyness.save()
                    work_timetable.save()
                    return redirect('home')
        else:
            # Вывод пустых форм
            return render(request, 'resume.html', {'resume_form': ResumeForm(),
                                                   'education_form': EducationForm(), 'about_job_form': AboutJobForm(),
                                                   'courses_form': CoursesForm(), 'tests_exams_form': TestsExamsForm()})
    else:
        return redirect('auth')


def go_to_sample(request, pk):
    """ Функция, используемая для отображения резюме. """
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Сохранение комментария и статуса в базе
            comment_text = request.POST.get('comment')
            status = request.POST.get('status')
            resume = Resume.objects.get(pk=pk)
            resume.moderator_comment = comment_text
            resume.moderation_status = status
            with transaction.atomic():
                resume.save(update_fields=['moderator_comment', 'moderation_status'])
            return redirect('home')
        else:
            # Вывод данных резюме
            resume = Resume.objects.filter(pk=pk).first()
            student = Students.objects.filter(id_student=resume.id_student.id_student).first()
            about_job = AboutJob.objects.filter(id_resume=resume.id_resume).first()
            specialization = Specialization.objects.filter(id_about_job=about_job.id_about_job)
            busyness = Busyness.objects.filter(id_about_job=about_job.id_about_job)
            work_timetable = WorkTimetable.objects.filter(id_about_job=about_job.id_about_job)
            educational_institution = EducationalInstitution.objects.filter(id_resume=resume.id_resume)
            photo = Photo.objects.get(id=student.photo.id)
            request.session['resume_choice'] = resume.id_resume
            return render(request, 'sample.html', {'student': student, 'resume': resume,
                                                   'about_job': about_job, 'specialization': specialization[0],
                                                   'busyness': busyness[0], 'work_timetable': work_timetable[0],
                                                   'educational_institution': educational_institution[0], 'photo': photo.image.name.split(sep='/')[1]})
    else:
        return redirect('auth')