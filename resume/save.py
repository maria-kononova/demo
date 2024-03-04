import datetime

from resume.dictionary import GENDER_CHOICES, TYPES_OF_COMMUNICATION_CHOICES, EDUCATION_LEVEL_CHOICES, \
    POSSIBILITY_OF_TRANSFER_CHOICES, BUSINESS_TRIPS_CHOICES, DESIRED_TIME_CHOICES
from resume.models import Students, Resume, EducationalInstitution


def create_student(student_form, user):
    new_student_id = Students.objects.all().count() + 1
    return Students(id_student=new_student_id, surname=student_form.cleaned_data.get('surname'),
                    name=student_form.cleaned_data.get('name'),
                    middle_name=student_form.cleaned_data.get('middle_name'),
                    birthdate=student_form.cleaned_data.get('birthday'),
                    gender=dict(GENDER_CHOICES).get(student_form.cleaned_data.get('gender')),
                    phone=student_form.cleaned_data.get('phone'),
                    email=student_form.cleaned_data.get('email'),
                    types_of_communication=dict(TYPES_OF_COMMUNICATION_CHOICES).get(
                        student_form.cleaned_data.get('types_of_communication')),
                    education_level=dict(EDUCATION_LEVEL_CHOICES).get(
                        student_form.cleaned_data.get('education_level')), id_auth_user=user)


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
                  date_of_creation=datetime.datetime.now())

def create_education(education_form, resume):
    education_new_id = EducationalInstitution.objects.all().count() + 1
    return  EducationalInstitution(id=education_new_id, id_resume=resume,
                           name_of_institution=education_form.cleaned_data.get(
                               'name_of_institution'),
                           faculty=education_form.cleaned_data.get('faculty'),
                           specialization=education_form.cleaned_data.get('specialization_of_institution'),
                           year_of_completion="2024",
                           level_education=dict(EDUCATION_LEVEL_CHOICES).get(
                               education_form.cleaned_data.get('level_education')))
