import datetime

from resume.dictionary import GENDER_CHOICES, TYPES_OF_COMMUNICATION_CHOICES, EDUCATION_LEVEL_CHOICES, \
    POSSIBILITY_OF_TRANSFER_CHOICES, BUSINESS_TRIPS_CHOICES, DESIRED_TIME_CHOICES, CURRENCY_CHOICES, \
    SPECIALIZATION_CHOICES, BUSYNESS_CHOICES, WORK_TIME_CHOICES
from resume.models import Students, Resume, EducationalInstitution, AboutJob, Specialization, Busyness, WorkTimetable, \
    Courses, TestsAndExams


def create_student(student_form, user, id):
    if not id:
        id = Students.objects.all().count() + 1
    return Students(id_student=id, surname=student_form.cleaned_data.get('surname'),
                    name=student_form.cleaned_data.get('name'),
                    middle_name=student_form.cleaned_data.get('middle_name'),
                    birthdate=student_form.cleaned_data.get('birthdate'),
                    gender=dict(GENDER_CHOICES).get(student_form.cleaned_data.get('gender')),
                    phone=student_form.cleaned_data.get('phone'),
                    email=student_form.cleaned_data.get('email'),
                    types_of_communication=dict(TYPES_OF_COMMUNICATION_CHOICES).get(
                        student_form.cleaned_data.get('types_of_communication')),
                    education_level=dict(EDUCATION_LEVEL_CHOICES).get(
                        student_form.cleaned_data.get('education_level')), user=user)


def create_resume(resume_form, student):
    new_resume_id = Resume.objects.all().count() + 1
    return Resume(id_resume=new_resume_id, id_student=student,
                  description_skills=resume_form.cleaned_data.get('description_skills'),
                  city=resume_form.cleaned_data.get('city'),
                  station_metro=resume_form.cleaned_data.get('station_metro'),
                  possibility_of_transfer=dict(POSSIBILITY_OF_TRANSFER_CHOICES).get(
                      resume_form.cleaned_data.get('possibility_of_transfer')),
                  business_trips=dict(BUSINESS_TRIPS_CHOICES).get(
                      resume_form.cleaned_data.get('business_trips')),
                  desired_time_in_the_way=dict(DESIRED_TIME_CHOICES).get(
                      resume_form.cleaned_data.get('desired_time_in_the_way')),
                  availability_car=resume_form.cleaned_data.get('availability_car'),
                  locale_resume=resume_form.cleaned_data.get('locale_resume'),
                  moderation_status='модерация',
                  date_of_creation=datetime.datetime.now())


def create_education(education_form, resume):
    education_new_id = EducationalInstitution.objects.all().count() + 1
    return EducationalInstitution(id=education_new_id, id_resume=resume,
                                  name_of_institution=education_form.cleaned_data.get(
                                      'name_of_institution'),
                                  faculty=education_form.cleaned_data.get('faculty'),
                                  specialization=education_form.cleaned_data.get('specialization_of_institution'),
                                  year_of_completion='2024', #!!!!!!!!!!!!!!
                                  level_education=dict(EDUCATION_LEVEL_CHOICES).get(
                                      education_form.cleaned_data.get('level_education')))


def create_courses(courses_form, resume):
    courses_new_id = Courses.objects.all().count() + 1
    return Courses(id=courses_new_id, id_resume=resume,
                                  organization=courses_form.cleaned_data.get(
                                      'name_of_organization_course'),
                                  course_name=courses_form.cleaned_data.get('name_of_course'),
                                  specialization=courses_form.cleaned_data.get('specialization_of_course'),
                                  year_of_completion='2024') #!!!!!!!!!!!!!!


def create_tests_exams(tests_exams_form, resume):
    tests_exams_new_id = EducationalInstitution.objects.all().count() + 1
    return TestsAndExams(id=tests_exams_new_id, id_resume=resume,
                                  organization=tests_exams_form.cleaned_data.get(
                                      'name_of_organization_test'),
                                  course_name=tests_exams_form.cleaned_data.get('name_of_test'),
                                  specialization=tests_exams_form.cleaned_data.get('specialization_of_test'),
                                  year_of_completion='2024') #!!!!!!!!!!!!!!


def create_about_job(about_job_form, resume):
    about_new_id = AboutJob.objects.all().count() + 1
    return AboutJob(id_about_job=about_new_id, id_resume=resume,
                    desired_position=about_job_form.cleaned_data.get('desired_position'),
                    desired_salary=about_job_form.cleaned_data.get('desired_salary'),
                    currency=dict(CURRENCY_CHOICES).get(about_job_form.cleaned_data.get('currency')))


def create_specialization(about_job_form, about_job):
    specialization_new_id = Specialization.objects.all().count() + 1
    return Specialization(id=specialization_new_id, id_about_job=about_job,
                          specialization=dict(SPECIALIZATION_CHOICES).get(
                              about_job_form.cleaned_data.get('specialization')))


def create_busyness(about_job_form, about_job):
    busyness_new_id = Busyness.objects.all().count() + 1
    return Busyness(id=busyness_new_id, id_about_job=about_job,
                    type_busyness=dict(BUSYNESS_CHOICES).get(
                        about_job_form.cleaned_data.get('busyness')))


def create_work_timetable(about_job_form, about_job):
    work_timetable_new_id = WorkTimetable.objects.all().count() + 1
    return WorkTimetable(id=work_timetable_new_id, id_about_job=about_job,
                         work_timetable=dict(WORK_TIME_CHOICES).get(
                             about_job_form.cleaned_data.get('work_timetable')))
