import os

import requests
import json

from django.shortcuts import redirect
from rest_framework import viewsets, generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Photo, ResumePhoto
from .serializers import PhotoSerializer, ImageSerializer, ChangePasswordSerializer
from resume.models import AuthUser, Students, Resume
from resume.permissions import IsOwnerOrReadOnly, IsOwner, IsOwnerStudent
from resume.serializers import StudentsSerializer, ResumesSerializer, UsersSerializer

HH_URL = 'https://api.hh.ru'
URL = "http://localhost:8080/"
CLIENT_ID = "VQVJ5QBD7OJ2L58U2ET8M7O8CNNEQSUM3F6T2D7RM449KETARC92PRRODBDN28S0"
CLIENT_SECRET = "JDUG1I830GU1JHKGSOFBVQGH03TG51IS284HP4RC536RJ99BJ2LMVAEHDS0SMLRT"

""" Обращение к API HH """


def get_from_url(url):
    j = requests.get(f"{HH_URL}{url}").json()
    # Загрузка JSON-строки в объект Python
    data = json.loads(json.dumps(j))
    # Получение списка имен объектов
    names_list = []
    for d in data:
        names_list.append((d['id'], d['name']))
    return names_list


def get_from_dictionaries(entity):
    j = requests.get(f"{HH_URL}/dictionaries").json()
    data = json.loads(json.dumps(j))
    names_list = [(d['id'], d['name']) for d in data[entity]]
    return names_list


def get_currency():
    j = requests.get(f"{HH_URL}/dictionaries").json()
    data = json.loads(json.dumps(j))
    names_list = [(d['code'], d['abbr']) for d in data["currency"]]
    return names_list


def get_specialization():
    j = requests.get(f"{HH_URL}/specializations").json()
    data = json.loads(json.dumps(j))
    list = [(item['id'], item['name']) for item in data]
    return list


def get_metro_stations(id):
    response = requests.get(f"{HH_URL}/metro/{id}")

    if response.status_code == 200:
        metro_stations = {}
        data = response.json()

        for line in data['lines']:
            for station in line['stations']:
                station_name = station['name']
                station_id = station['id']

                metro_stations[station_id] = station_name

        if metro_stations:
            list = []
            for station_id, station_name in metro_stations.items():
                station_choice = (station_id, station_name)
                list.append(station_choice)

        return list
    else:
        return None


# Метод создания резюме на HH
def create_resume_on_hh(auth_token, resume_data):
    url = HH_URL + "/resumes"
    headers = {
        "Authorization": "Bearer " + auth_token,
        "User-Agent": "Resume",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=resume_data)

    if response.status_code == 201:
        return "Резюме успешно создано на HeadHunter"
    else:
        return "Ошибка при создании резюме на HeadHunter: {}".format(response.text)


def get_access_token_app(url, client_id, client_secret):
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    return response.json()["access_token"]


def get_access_token(auth_token, pk):
    response = requests.post(
        "https://api.hh.ru/token",
        data={"grant_type": "authorization_code", "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET,
              "redirect_uri": URL + f"resume/access/{pk}/", "code": auth_token}
    )
    print(response.json())
    return response.json()["access_token"]


# def authenticate_user(username, password):
#     url = 'https://api.hh.ru/oauth/token'
#     data = {
#         'grant_type': 'password',
#         'username': username,
#         'password': password,
#         'client_id': 'your_client_id',
#         'client_secret': 'your_client_secret'
#     }
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
#
#     response = requests.post(url, data=data, headers=headers)
#
#     if response.status_code == 200:
#         access_token = response.json()['access_token']
#         return access_token
#     else:
#         return response.status_code
#
#
# def auth_app():
#     url = 'https://api.hh.ru/vacancies'
#     headers = {
#         'User-Agent': 'Ваше приложение',
#         'Authorization': 'Bearer ваш_api_ключ'
#     }
#
#     response = requests.get(url, headers=headers)
#
#     if response.status_code == 200:
#         print('Запрос успешно выполнен')
#     else:
#         print('Ошибка при выполнении запроса:', response.text)


""" Методы API """


# Students POST
class StudentsAPICreate(generics.ListCreateAPIView):
    serializer_class = StudentsSerializer
    permission_classes = (IsAuthenticated,)

    # GET информации о возможности создания нового пользователя
    def get(self, request, *args, **kwargs):
        user = self.request.user
        existing_record = Students.objects.filter(user=user).first()
        if existing_record:
            student = Students.objects.filter(user=self.request.user).first()
            return Response(
                {"message": "У Вас уже есть запись о личных данных. Вы можете обновить личные данные по ссылке:",
                 "url": URL + "resume/api/v1/students/update/" + str(student.id_student)}, status=200)
        custom_result = {'message': 'You can create a new student.'}
        return Response(custom_result)

    # Добавления id студента в ответ
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Дополнительная логика
        student = Students.objects.filter(user=self.request.user).first()
        additional_data = {
            'ID': str(student.id_student)
        }
        response.data.update(additional_data)
        return response

    # Проверка и создание нового студента
    def perform_create(self, serializer):
        student = Students.objects.filter(user=self.request.user).first()
        if not student:
            serializer.save(user=self.request.user)
        else:
            return Response(
                {"message": "У Вас уже есть запись о личных данных. Вы можете обновить личные данные по ссылке:",
                 "url": URL + "resume/api/v1/students/update/" + str(student.id_student)}, status=400)


# Students GET
class StudentsAPIView(generics.RetrieveAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = (IsOwner,)


# Students PUT
class StudentsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = (IsOwner,)

    # добавление данных о ID при UPDATE
    def perform_update(self, serializer):
        student = Students.objects.filter(user=self.request.user).first()
        serializer.save(id_student=student.id_student, user=self.request.user)


# Students DELETE
class StudentsAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = (IsOwner,)


# GET id студента
class StudentsAPIViewID(APIView):
    def get(self, request):
        student = Students.objects.filter(user=self.request.user).first()
        if student:
            return Response({'ID': student.id_student}, status=200)
        return Response({"message": "У Вас нет записи о личных данных. Вы можете создать ей по ссылке:",
                         "url": URL + "resume/api/v1/students/create/"}, status=400)


# GET списка ID resume
class ResumesAPIView(generics.RetrieveAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumesSerializer
    permission_classes = (IsOwnerStudent,)


class ResumesIDAPIView(APIView):
    def get(self, request):
        user = request.user
        student = Students.objects.filter(user=user).first()
        resumes_id = Resume.objects.filter(id_student=student)
        current_user_resume_ids = [resume.id_resume for resume in resumes_id]
        return Response({'id': current_user_resume_ids})


# PUT обновление данных user username
class UsersAPIUpdate(APIView):
    def get(self, request):
        user = AuthUser.objects.filter(id=self.request.user.id).first()
        if user:
            return Response({'ID': user.id, "username": user.username}, status=200)
        return Response({"message": "У вас нет записи."}, status=400)

    def put(self, request, *args, **kwargs):
        user = AuthUser.objects.filter(id=self.request.user.id).first()
        if user:
            try:
                instance = AuthUser.objects.get(pk=user.id)
            except:
                return Response({"error": "Нет объекта"}, status=404)
        serializer = UsersSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({"user": serializer.data, 'token': token.key}, status=status.HTTP_200_OK)


# PUT обновление данных user password
class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# Метод обращения к API Post-запрос
def post_request(url, data, token):
    url = URL + url
    headers = {'Authorization': 'Token ' + token, 'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.json())


def get_token(username, password):
    url = URL + 'resume/api/v1/auth/token/login/'
    body = {'username': username, 'password': password}
    response = requests.post(url, data=json.dumps(body))
    print(response.json())


# POST Загрузка фотографии студента
class PhotoUploadView(APIView):
    # permission_classes = (IsOwnerStudent,)
    def post(self, request):
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # получения студента для сохранения id изображения
            student = Students.objects.filter(user=request.user).first()
            student.photo = ResumePhoto.objects.filter(id=serializer.data['id']).first()
            student.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
