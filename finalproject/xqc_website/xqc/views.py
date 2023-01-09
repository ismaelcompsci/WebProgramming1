from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from .utils import *
import json


# Create your views here.

def index(request):
    return render(request, "xqc/index.html")


def stream(request):
    return render(request, "xqc/stream.html")




def get_stream(request, channel):
    if request.method == "GET":
        data = is_live(channel)
        return JsonResponse(data)

@csrf_exempt
def get_userlogs(request):
    if request.method == "POST":
        username = request.POST["username"]
        data = get_user_chat_logs(username)
        return JsonResponse(data, safe=False)