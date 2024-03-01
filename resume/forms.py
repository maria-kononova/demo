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
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class TestForm(forms.Form):
    title = forms.CharField(label='Название резюме', max_length=45)
    surname = forms.CharField(label='Фамилия', max_length=30)
    name = forms.CharField(label='Имя', max_length=30)
    middle_name = forms.CharField(label='Отчество', max_length=30, required=False)
    photo = forms.ImageField(label='Фото')
    birthday = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=range(year, year-101, -1)))
    gender = forms.ChoiceField(label='Пол', choices=GENDER_CHOICES)
    phone = forms.CharField(label='Телефон', max_length=12)
    email = forms.EmailField(label='Почта')
    types_of_communication = forms.ChoiceField(label='Вид связи', choices=TYPES_OF_COMMUNICATION_CHOICES)
    education_level = forms.ChoiceField(label='Уровень образования', choices=EDUCATION_LEVEL_CHOICES)

