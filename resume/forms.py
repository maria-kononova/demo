from datetime import timezone, datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

year = datetime.now().year

# Выбор пола
GENDER_CHOICES = (
    (1, "Мужской"),
    (2, "Женский"),
)

# Выбор вида связи
TYPES_OF_COMMUNICATION_CHOICES = (
    (1, "Телефон"),
    (2, "Почта"),
)

# Выбор уровня образования
EDUCATION_LEVEL_CHOICES = (
    (1, "Среднее"),
    (2, "Среднее специальное"),
    (3, "Неоконченное высшее"),
    (4, "Высшее"),
    (5, "Бакалавр"),
    (6, "Магистр"),
    (7, "Кандидат наук"),
    (8, "Доктор наук"),
)

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "myfield"}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={"class":"myfield field-email"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "myfield"}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={"class": "myfield"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class":"myfield"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class":"myfield"}))


class TestForm(forms.Form):
    title = forms.CharField(label='Название резюме', max_length=45, widget=forms.TextInput(attrs={"class":"myfield"}))
    surname = forms.CharField(label='Фамилия', max_length=30, widget=forms.TextInput(attrs={"class":"myfield"}))
    name = forms.CharField(label='Имя', max_length=30, widget=forms.TextInput(attrs={"class":"myfield"}))
    middle_name = forms.CharField(label='Отчество', max_length=30, required=False, widget=forms.TextInput(attrs={"class":"myfield"}))
    photo = forms.FileField(label='Фото', widget=forms.FileInput(attrs={"class":"myfield_select"}))
    birthday = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=range(year, year-101, -1), attrs={"class":"myfield_select"}))
    gender = forms.ChoiceField(label='Пол', choices=GENDER_CHOICES, widget=forms.Select(attrs={"class":"myfield_select"}))
    phone = forms.CharField(label='Телефон', max_length=12, widget=forms.TextInput(attrs={"class":"myfield"}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={"class":"myfield field-email"}))
    types_of_communication = forms.ChoiceField(label='Вид связи', choices=TYPES_OF_COMMUNICATION_CHOICES, widget=forms.Select(attrs={"class":"myfield_select"}))
    education_level = forms.ChoiceField(label='Уровень образования', choices=EDUCATION_LEVEL_CHOICES, widget=forms.Select(attrs={"class":"myfield_select"}))

