from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from .utils import *
from .models import *
import json


# Create your views here.


def index(request):
    return render(request, "xqc/index.html")


def stream(request):
    return render(request, "xqc/stream.html")


def get_userlogs(request):
    return render(request, "xqc/chatlogs.html")


def offline_chat(request):
    return render(request, "xqc/offline.html")


def get_stream(request, channel):
    if request.method == "GET":
        data = is_live(channel)
        return JsonResponse(data)


@csrf_exempt
def user_logger(request):
    if request.method == "POST":
        username = json.loads(request.body)
        api_iter("leamsi_1")
        return JsonResponse({"sent": "Sent Successfully"}, status=201)
