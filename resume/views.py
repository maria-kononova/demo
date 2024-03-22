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

from .models import Test, Students, AuthUser, Resume, EducationalInstitution, AboutJob, Specialization, Busyness, \
    WorkTimetable
from .create_object import create_student, create_resume, create_education, create_about_job, create_specialization, \
    create_busyness, create_work_timetable


# Create your views here.
# request.session.flush() или response.delete_cookie('sessionid') или logout(request) для завершения сессии пользователя
def home(request):
    if request.user.is_authenticated:
        user= request.user
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


def myresume(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            resume_form = ResumeForm(request.POST)
            education_form = EducationForm(request.POST)
            about_job_form = AboutJobForm(request.POST)
            if resume_form.is_valid() and education_form.is_valid() and about_job_form.is_valid():
                user= request.user
                student = Students.objects.filter(user=user).first()
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
        return redirect('auth')


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
                return redirect('home')
                # return render(request, 'home.html', {
                #     'user_type': user_type})  # Перенаправление на страницу "home" с передачей типа пользователя в контексте
            else:
                form = UserLoginForm()
                return render(request, 'login.html', {'form': form, 'msg': "Пароль или имя пользователя неверное"})
        else:
            form = UserLoginForm()
        return render(request, 'login.html', {'form': form, 'msg': ""})
    else:
        return redirect('home')
        # user_type = 'Модератор' if request.user.is_staff == 1 else 'Студент'
        # return render(request, 'home.html', {'user_type': user_type})


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

def submit_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        status = request.POST.get('status')
        # Дополнительная логика для обработки комментария и статуса резюме

        # Пример сохранения комментария в базе данных
        resume_comment = ResumeComment(comment=comment_text, status=status)
        resume_comment.save()

        # Перенаправление на другую страницу или обновление текущей
        return HttpResponseRedirect('/resume/1/sample')  # Измените URL на нужный вам

    # Логика для GET-запроса, если необходимо
    return render(request, 'sample.html', {})  # Перенаправление на текущую страницу с пустым контекстом


def exit(request):
    request.session.flush()
    return redirect('auth')


def go_to_sample(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return redirect('go_to_sample')
        else:
            # Вывод данных резюме
            resume = Resume.objects.filter(pk=pk).first()
            student = Students.objects.filter(id_student=resume.id_student.id_student).first()
            about_job = AboutJob.objects.filter(id_resume=resume.id_resume).first()
            specialization = Specialization.objects.filter(id_about_job=about_job.id_about_job)
            busyness = Busyness.objects.filter(id_about_job=about_job.id_about_job)
            work_timetable = WorkTimetable.objects.filter(id_about_job=about_job.id_about_job)
            educational_institution = EducationalInstitution.objects.filter(id_resume=resume.id_resume)
            return render(request, 'sample.html', {'student': student, 'resume': resume,
                                                   'about_job': about_job, 'specialization': specialization[0],
                                                   'busyness': busyness[0], 'work_timetable': work_timetable[0],
                                                   'educational_institution': educational_institution[0]})
    else:
        return redirect('auth')


def account(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Сохранение данных пользователя
            print(list(request.POST.items()))
            student_form = StudentForm(request.POST)
            if student_form.is_valid():
                print(student_form.cleaned_data)
                user = request.user
                student = create_student(student_form, user, None)
                with transaction.atomic():
                    student.save()
                return redirect('account')
        else:
            # Вывод данных пользователя
            update_check = 0
            user = request.user
            studentList = Students.objects.filter(user=user)
            return render(request, 'account.html',
                          {'student': studentList, 'student_form_account': StudentForm(), 'update_check': update_check})
    else:
        return redirect('auth')


def account_edit(request):
    if request.user.is_authenticated:
        # student = get_object_or_404(Students, pk=pk)
        user = request.user
        update_check = 1
        if request.method == "POST":
            if 'edit_btn' in request.POST:
                # Сохранение измененных данных
                # form = StudentForm(request.POST, instance=student)
                student_form = StudentForm(request.POST)
                if student_form.is_valid():
                    id_student = Students.objects.filter(user=user).first().id_student
                    student = create_student(student_form, user, id_student)
                    with transaction.atomic():
                        student.save(update_fields=['surname', 'name', 'middle_name', 'birthdate', 'gender', 'phone', 'email',
                                                    'types_of_communication', 'education_level'])
                        return redirect('account')
        else:
            # Вывод формы для изменения данных (сами данные из бд пока не выгружаются для редактирования)
            # form = StudentForm(instance=student)
            studentList = Students.objects.filter(user=user)
            return render(request, 'account.html',
                          {'student': studentList, 'student_form_account': StudentForm(), 'update_check': update_check})
    else:
        return redirect('auth')
