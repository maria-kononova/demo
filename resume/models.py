from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# таблицы django
class AboutJob(models.Model):
    id_about_job = models.IntegerField(db_column='ID_about_job', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.CASCADE, db_column='ID_resume')  # Field name made lowercase.
    desired_position = models.CharField(db_column='Desired_position', max_length=45)  # Field name made lowercase.
    desired_salary = models.IntegerField(db_column='Desired_salary', blank=True,
                                         null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'about_job'


class AuthUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=128)  # Field name made lowercase.
    last_login = models.DateTimeField(db_column='Last_login', blank=True, null=True)  # Field name made lowercase.
    is_superuser = models.IntegerField(db_column='Is_superuser')  # Field name made lowercase.
    username = models.CharField(db_column='Username', unique=True, max_length=150)  # Field name made lowercase.
    first_name = models.CharField(db_column='First_name', max_length=150)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_name', max_length=150)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=254)  # Field name made lowercase.
    is_staff = models.IntegerField(db_column='Is_staff')  # Field name made lowercase.
    is_active = models.IntegerField(db_column='Is_active')  # Field name made lowercase.
    date_joined = models.DateTimeField(db_column='Date_joined')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'auth_user'


class Busyness(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_about_job = models.ForeignKey(AboutJob, models.CASCADE, db_column='ID_about_job')  # Field name made lowercase.
    type_busyness = models.CharField(db_column='Type_busyness', max_length=45, blank=True,
                                     null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'busyness'


class Citizenship(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_student = models.ForeignKey('Students', models.CASCADE, db_column='ID_student')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'citizenship'


class Courses(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.CASCADE, db_column='ID_resume')  # Field name made lowercase.
    organization = models.CharField(db_column='Organization', max_length=45)  # Field name made lowercase.
    course_name = models.CharField(db_column='Course_name', max_length=45)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=45)  # Field name made lowercase.
    year_of_completion = models.CharField(db_column='Year_of_completion', max_length=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'courses'


class EducationalInstitution(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.CASCADE, db_column='ID_resume')  # Field name made lowercase.
    name_of_institution = models.CharField(db_column='Name_of_institution', max_length=45)  # Field name made lowercase.
    faculty = models.CharField(db_column='Faculty', max_length=45, blank=True, null=True)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=45)  # Field name made lowercase.
    year_of_completion = models.CharField(db_column='Year_of_completion', max_length=4)  # Field name made lowercase.
    level_education = models.CharField(db_column='Level_education', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'educational_institution'


class KeySkills(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.CASCADE, db_column='ID_resume')  # Field name made lowercase.
    skill = models.CharField(db_column='Skill', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'key_skills'


class Languages(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_student = models.ForeignKey('Students', models.CASCADE, db_column='ID_student')  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=45)  # Field name made lowercase.
    proficiency_level = models.CharField(db_column='Proficiency_level', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'languages'


class Portfolio(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.CASCADE, db_column='ID_resume')  # Field name made lowercase.
    photo = models.CharField(db_column='Photo', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'portfolio'


class Resume(models.Model):
    id_resume = models.IntegerField(db_column='ID_resume', primary_key=True)  # Field name made lowercase.
    id_student = models.ForeignKey('Students', models.CASCADE, db_column='ID_student')  # Field name made lowercase.
    description_skills = models.CharField(db_column='Description_skills', max_length=700, blank=True,
                                          null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=45, blank=True, null=True)  # Field name made lowercase.
    station_metro = models.CharField(db_column='Station_metro', max_length=45, blank=True,
                                     null=True)  # Field name made lowercase.
    possibility_of_transfer = models.CharField(db_column='Possibility_of_transfer',
                                               max_length=45)  # Field name made lowercase.
    business_trips = models.CharField(db_column='Business_trips', max_length=45)  # Field name made lowercase.
    desired_time_in_the_way = models.CharField(db_column='Desired_time_in_the_way',
                                               max_length=45)  # Field name made lowercase.
    availability_car = models.IntegerField(db_column='Availability_car')  # Field name made lowercase.
    locale_resume = models.CharField(db_column='Locale_resume', max_length=45)  # Field name made lowercase.
    date_of_creation = models.DateTimeField(db_column='Date_of_creation')  # Field name made lowercase.
    moderation_status = models.CharField(db_column='Moderation_status', max_length=45)  # Field name made lowercase.
    moderator_comment = models.CharField(db_column='Moderator_comment', max_length=300,
                                         blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'resume'


class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'role'


class Specialization(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_about_job = models.ForeignKey(AboutJob, models.CASCADE, db_column='ID_about_job')  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'specialization'


# class Students(models.Model):
#     id_student = models.IntegerField(db_column='ID_student', primary_key=True)  # Field name made lowercase.
#     surname = models.CharField(db_column='Surname', max_length=30)  # Field name made lowercase.
#     name = models.CharField(db_column='Name', max_length=30)  # Field name made lowercase.
#     middle_name = models.CharField(db_column='Middle_name', max_length=30, blank=True,
#                                    null=True)  # Field name made lowercase.
#     birthdate = models.DateField(db_column='Birthdate', blank=True, null=True)  # Field name made lowercase.
#     gender = models.CharField(db_column='Gender', max_length=7)  # Field name made lowercase.
#     photo = models.FileField(db_column='Photo', blank=True, null=True)  # Field name made lowercase.
#     phone = models.CharField(db_column='Phone', max_length=12)  # Field name made lowercase.
#     email = models.CharField(db_column='Email', max_length=45)  # Field name made lowercase.
#     types_of_communication = models.CharField(db_column='Types_of_communication',
#                                               max_length=45)  # Field name made lowercase.
#     education_level = models.CharField(db_column='Education_level', max_length=45)  # Field name made lowercase.
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)  # Field name made lowercase.
#
#     class Meta:
#         managed = False
#         db_table = 'students'

class ResumePhoto(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'resume_photo'


class Students(models.Model):
    id_student = models.AutoField(db_column='ID_student', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    surname = models.CharField(db_column='Surname', max_length=30)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)  # Field name made lowercase.
    middle_name = models.CharField(db_column='Middle_name', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    birthdate = models.DateField(db_column='Birthdate')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=7)  # Field name made lowercase.
    photo = models.ForeignKey(ResumePhoto, models.DO_NOTHING, db_column='Photo', blank=True,
                              null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=12)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=45)  # Field name made lowercase.
    types_of_communication = models.CharField(db_column='Types_of_communication',
                                              max_length=45)  # Field name made lowercase.
    education_level = models.CharField(db_column='Education_level', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'students'


class Test(models.Model):
    title = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class TestsAndExams(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey(Resume, models.CASCADE, db_column='ID_resume')  # Field name made lowercase.
    organization = models.CharField(db_column='Organization', max_length=45)  # Field name made lowercase.
    course_name = models.CharField(db_column='Course_name', max_length=45)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=45)  # Field name made lowercase.
    year_of_completion = models.CharField(db_column='Year_of_completion', max_length=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tests_and_exams'


class WorkExperience(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey(Resume, models.CASCADE, db_column='ID_resume')  # Field name made lowercase.
    organization = models.CharField(db_column='Organization', max_length=45)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    industries = models.CharField(db_column='Industries', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    occupied_position = models.CharField(db_column='Occupied_position', max_length=45)  # Field name made lowercase.
    start_work = models.DateTimeField(db_column='Start_work')  # Field name made lowercase.
    end_work = models.DateTimeField(db_column='End_work')  # Field name made lowercase.
    descriptionres_ponsibilities_and_achievements = models.CharField(
        db_column='Descriptionres_ponsibilities_and_achievements', max_length=500, blank=True,
        null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'work_experience'


class WorkResolution(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_student = models.ForeignKey(Students, models.CASCADE, db_column='ID_student')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'work_resolution'


class WorkTimetable(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_about_job = models.ForeignKey(AboutJob, models.CASCADE, db_column='ID_about_job')  # Field name made lowercase.
    work_timetable = models.CharField(db_column='Work_timetable', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'work_timetable'


class Photo(models.Model):
    image = models.ImageField(upload_to='photo')
