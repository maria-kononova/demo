from django.shortcuts import render
import requests
from django.template import loader
from django.http import HttpResponse

from resume.models import Students


# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    context = {}
    return HttpResponse(template.render(context, request))


def myresume(request):
    template = loader.get_template('resume.html')
    context = {} #'student': Students.objects.all().first()
    return HttpResponse(template.render(context, request))
