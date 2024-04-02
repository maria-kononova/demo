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
URL = "http://localhost:8000/"

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
    # Загрузка JSON-строки в объект Python
    data = json.loads(json.dumps(j))
    # Получение списка имен объектов
    names_list = [(d['id'], d['name']) for d in data[entity]]
    return names_list


def get_currency():
    j = requests.get(f"{HH_URL}/dictionaries").json()
    # Загрузка JSON-строки в объект Python
    data = json.loads(json.dumps(j))
    # Получение списка имен объектов
    names_list = [(d['code'], d['abbr']) for d in data["currency"]]
    return names_list


def get_specialization():
    j = requests.get(f"{HH_URL}/specializations").json()
    data = json.loads(json.dumps(j))
    # Извлечение данных в виде списка кортежей (id, name)
    # list = []
    # for item in data:
    #     for spec in item['specializations']:
    #         list.append((spec['id'], spec['name']))
    list = [(item['id'], item['name']) for item in data]
    return list


def auth():
    # client_id = "VQVJ5QBD7OJ2L58U2ET8M7O8CNNEQSUM3F6T2D7RM449KETARC92PRRODBDN28S0"
    # client_secret = "JDUG1I830GU1JHKGSOFBVQGH03TG51IS284HP4RC536RJ99BJ2LMVAEHDS0SMLRT"
    # # NO339LH7AML4HME1A7EPBD25P432HM64CT9ER92LBRRO9UNJO7F0DF4P7RNPM0FP
    # access_token = requests.post('https://hh.ru/oauth/token',
    #                              {'grant_type': 'authorization_code', 'client_id': client_id,
    #                               'client_secret': client_secret, 'code': '<CODE>'}).json()
    #
    # print(access_token)
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    # }
    # r = requests.get("https://hh.ru", headers=headers)
    # print(r)
    url = 'https://moscow.hh.ru/account/login'

    # Важно. По умолчанию requests отправляет вот такой
    # заголовок 'User-Agent': 'python-requests/2.22.0 ,  а это приводит к тому , что Nginx
    # отправляет 404 ответ. Поэтому нам нужно сообщить серверу, что запрос идет от браузера

    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    # Создаем сессию и указываем ему наш user-agent
    session = requests.Session()
    r = session.get(url, headers={
        'User-Agent': user_agent_val
    })

    # Указываем referer. Иногда , если не указать , то приводит к ошибкам.
    session.headers.update({'Referer': url})

    # Хотя , мы ранее указывали наш user-agent и запрос удачно прошел и вернул
    # нам нужный ответ, но user-agent изменился на тот , который был
    # по умолчанию. И поэтому мы обновляем его.
    session.headers.update({'User-Agent': user_agent_val})

    # Получаем значение _xsrf из cookies
    _xsrf = session.cookies.get('_xsrf', domain=".hh.ru")

    # Осуществляем вход с помощью метода POST с указанием необходимых данных
    post_request = session.post(url, {
        'backUrl': 'https://spb.hh.ru/',
        'username': '515nonia515@gmail.com',
        'password': '228338118',
        '_xsrf': _xsrf,
        'remember': 'yes',
    })
    url = post_request.json()['redirectUrl']

    # Вход успешно воспроизведен и мы сохраняем страницу в html файл
    with open("hh_success.html", "w", encoding="utf-8") as f:
        f.write(post_request.text)

    return post_request.json()['redirectUrl']


def get_access_token(url, client_id, client_secret):
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    return response.json()["access_token"]


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
