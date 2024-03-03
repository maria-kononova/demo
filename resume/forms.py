from datetime import timezone, datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from resume.dictionary import GENDER_CHOICES, TYPES_OF_COMMUNICATION_CHOICES, EDUCATION_LEVEL_CHOICES, CITY_CHOICES, \
    STATION_METRO_CHOICES, POSSIBILITY_OF_TRANSFER_CHOICES, BUSINESS_TRIPS_CHOICES, DESIRED_TIME_CHOICES, \
    DRIVING_LISENSE_CHOICES, LOCALE_RESUME_CHOICES, SPECIALIZATION_CHOICES, CURRENCY_CHOICES, BUSYNESS_CHOICES, \
    WORK_TIME_CHOICES

year = datetime.now().year

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


class ResumeForm(forms.Form):
    #title = forms.CharField(label='Название резюме', max_length=45, widget=forms.TextInput(attrs={"class":"myfield"}))
    surname = forms.CharField(label='Фамилия', max_length=30, widget=forms.TextInput(attrs={"class": "myfield"}))
    name = forms.CharField(label='Имя', max_length=30, widget=forms.TextInput(attrs={"class": "myfield"}))
    middle_name = forms.CharField(label='Отчество', max_length=30, widget=forms.TextInput(attrs={"class": "myfield"}))
    #photo = forms.FileField(label='Фото', widget=forms.FileInput(attrs={"class": "myfield_select"}))
    birthday = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=range(year, year-101, -1), attrs={"class": "myfield_select"}))
    gender = forms.ChoiceField(label='Пол', choices=GENDER_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    phone = forms.CharField(label='Телефон', max_length=12, widget=forms.TextInput(attrs={"class": "myfield"}))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={"class": "myfield field-email"}))
    types_of_communication = forms.ChoiceField(label='Вид связи', choices=TYPES_OF_COMMUNICATION_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    education_level = forms.ChoiceField(label='Уровень образования', choices=EDUCATION_LEVEL_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))

    # Гражданство
    #country_citizen_chip = forms.ChoiceField(label='Гражданство', choices=COUNTRY_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))

    # Разрешение на работу
    #country_work_resolution = forms.ChoiceField(label='Разрешение на работу', choices=COUNTRY_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))

    # Языки
    #language = forms.ChoiceField(label='Язык', choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    #proficiency_level = forms.ChoiceField(label='Уровень владения', choices=PROFICIENCY_LEVEL_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))

    # Резюме
    description_skills = forms.CharField(label='Описание скиллов', max_length=700, widget=forms.Textarea(attrs={"class": "myfield"}))
    city = forms.ChoiceField(label='Город', choices=CITY_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    station_metro = forms.ChoiceField(label='Станция метро', choices=STATION_METRO_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    # Нужно добавить место для переезда / коммандировки
    possibility_of_transfer = forms.ChoiceField(label='Переезд', choices=POSSIBILITY_OF_TRANSFER_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    business_trips = forms.ChoiceField(label='Готовность к командировкам', choices=BUSINESS_TRIPS_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    desired_time_in_the_way = forms.ChoiceField(label='Желаемое время в пути', choices=DESIRED_TIME_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    # На hh.ru их можно выбрать несколько...
    driving_license = forms.ChoiceField(label='Водительские права', choices=DRIVING_LISENSE_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    availability_car = forms.BooleanField(label='Наличие автомобиля', required=False, initial=False, widget=forms.CheckboxInput())
    locale_resume = forms.ChoiceField(label='Локаль резюме', choices=LOCALE_RESUME_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))

    # О работе
    desired_position = forms.CharField(label='Желаемая должность', max_length=50, widget=forms.TextInput(attrs={"class": "myfield"}))
    # Их тоже несколько
    specialization = forms.ChoiceField(label='Специализация', choices=SPECIALIZATION_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    desired_salary = forms.IntegerField(label='Желаемая зарплата', max_value=1000000, widget=forms.NumberInput(attrs={'size':'7', "class": "myfield field_salary"}))
    currency = forms.ChoiceField(label='Валюта', choices=CURRENCY_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    # Их тоже несколько
    busyness = forms.ChoiceField(label='Занятость', choices=BUSYNESS_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))
    work_timetable = forms.ChoiceField(label='График работы', choices=WORK_TIME_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))

    # Учебное заведение
    name_of_institution = forms.CharField(label='Название учебного заведения', max_length=30, widget=forms.TextInput(attrs={"class": "myfield"}))
    faculty = forms.CharField(label='Факультет', max_length=30, widget=forms.TextInput(attrs={"class": "myfield"}))
    specialization_of_institution = forms.CharField(label='Специальность', max_length=30, widget=forms.TextInput(attrs={"class": "myfield"}))
    #Пока не разобралась как оставить только год
    year_of_completion_institution = forms.DateField(label='Год окончания', widget=forms.SelectDateWidget(years=range(year, year - 101, -1),
                                                                                     attrs={"class": "myfield_select"}))
    level_education = forms.ChoiceField(label='Ступень образования', choices=EDUCATION_LEVEL_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))

    # Ключевые навыки
    #skill = forms.ChoiceField(label='Ключевые навыки', choices=SKILL_CHOICES, widget=forms.Select(attrs={"class": "myfield_select"}))

    # Портфолио
    #photo_portfolio = forms.FileField(label='Фото для портфолио', widget=forms.FileInput(attrs={"class": "myfield_select"}))




