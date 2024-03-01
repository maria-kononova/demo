from django.db import models


# Create your models here.
# таблицы django
class AboutJob(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.DO_NOTHING, db_column='ID_resume')  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=45)  # Field name made lowercase.
    desired_position = models.CharField(db_column='Desired_position', max_length=45)  # Field name made lowercase.
    desired_salary = models.IntegerField(db_column='Desired_salary', blank=True,
                                         null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    busyness = models.CharField(db_column='Busyness', max_length=45, blank=True,
                                null=True)  # Field name made lowercase.
    work_timetable = models.CharField(db_column='Work_timetable', max_length=45, blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'about_job'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Citizenship(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_student = models.ForeignKey('Students', models.DO_NOTHING, db_column='ID_student')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'citizenship'


class Courses(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.DO_NOTHING, db_column='ID_resume')  # Field name made lowercase.
    organization = models.CharField(db_column='Organization', max_length=45)  # Field name made lowercase.
    course_name = models.CharField(db_column='Course_name', max_length=45)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=45)  # Field name made lowercase.
    year_of_completion = models.CharField(db_column='Year_of_completion', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'courses'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


# Наша бд
class EducationalInstitution(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.DO_NOTHING, db_column='ID_resume')  # Field name made lowercase.
    name_of_institution = models.CharField(db_column='Name_of_institution', max_length=45)  # Field name made lowercase.
    faculty = models.CharField(db_column='Faculty', max_length=45, blank=True, null=True)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=45)  # Field name made lowercase.
    year_of_completion = models.CharField(db_column='Year_of_completion', max_length=45)  # Field name made lowercase.
    level_education = models.CharField(db_column='Level_education', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'educational_institution'


class KeySkills(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.DO_NOTHING, db_column='ID_resume')  # Field name made lowercase.
    skill = models.CharField(db_column='Skill', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'key_skills'


class Languages(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_student = models.ForeignKey('Students', models.DO_NOTHING, db_column='ID_student')  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=45)  # Field name made lowercase.
    proficiency_level = models.CharField(db_column='Proficiency_level', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'languages'


class Portfolio(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey('Resume', models.DO_NOTHING, db_column='ID_resume')  # Field name made lowercase.
    photo = models.CharField(db_column='Photo', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'portfolio'


class Resume(models.Model):
    id_resume = models.IntegerField(db_column='ID_resume', primary_key=True)  # Field name made lowercase.
    id_student = models.ForeignKey('Students', models.DO_NOTHING, db_column='ID_student')  # Field name made lowercase.
    description_skills = models.CharField(db_column='Description_skills', max_length=500, blank=True,
                                          null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=45, blank=True, null=True)  # Field name made lowercase.
    station_metro = models.CharField(db_column='Station_metro', max_length=45, blank=True,
                                     null=True)  # Field name made lowercase.
    possibility_of_transfer = models.IntegerField(db_column='Possibility_of_transfer')  # Field name made lowercase.
    business_trips = models.IntegerField(db_column='Business_trips')  # Field name made lowercase.
    desired_time_in_the_way = models.CharField(db_column='Desired_time_in_the_way',
                                               max_length=45)  # Field name made lowercase.
    driving_license = models.CharField(db_column='Driving_license', max_length=45)  # Field name made lowercase.
    availability_car = models.IntegerField(db_column='Availability_car')  # Field name made lowercase.
    locale_resume = models.CharField(db_column='Locale_resume', max_length=45, blank=True,
                                     null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'resume'


class Students(models.Model):
    id_student = models.IntegerField(db_column='ID_student', primary_key=True)  # Field name made lowercase.
    surname = models.CharField(db_column='Surname', max_length=30)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)  # Field name made lowercase.
    middle_name = models.CharField(db_column='Middle_name', max_length=30, blank=True,
                                   null=True)  # Field name made lowercase.
    birthdate = models.DateField(db_column='Birthdate', blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=7, blank=True, null=True)  # Field name made lowercase.
    photo = models.TextField(db_column='Photo', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=12)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=45, blank=True, null=True)  # Field name made lowercase.
    types_of_communication = models.CharField(db_column='Types_of_communication',
                                              max_length=10)  # Field name made lowercase.
    education_level = models.CharField(db_column='Education_level', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'students'


class TestsAndExams(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey(Resume, models.DO_NOTHING, db_column='ID_resume')  # Field name made lowercase.
    organization = models.CharField(db_column='Organization', max_length=45)  # Field name made lowercase.
    course_name = models.CharField(db_column='Course_name', max_length=45)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=45)  # Field name made lowercase.
    year_of_completion = models.CharField(db_column='Year_of_completion', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tests_and_exams'


class WorkExperience(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id_resume = models.ForeignKey(Resume, models.DO_NOTHING, db_column='ID_resume')  # Field name made lowercase.
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
    id_student = models.ForeignKey(Students, models.DO_NOTHING, db_column='ID_student')  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'work_resolution'


# пользователь
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    role = models.ForeignKey('Role', models.DO_NOTHING, db_column='role')

    class Meta:
        managed = False
        db_table = 'user'


class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'role'


class Test(models.Model):
    title = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'
