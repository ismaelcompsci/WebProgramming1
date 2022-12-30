from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json

from .utils import *
from .models import *



def index(request):
    if request.method == "POST":
        post = post_maker(request, request.user)
        new_post = Post(post_creator=post["post_creator"], text=post["text"], date=post["date"])
        new_post.save()

    posts = Post.objects.all().order_by("-date")

    paginator = Paginator(posts, 10)

    page = request.GET.get("page")

    print(page)

    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, "network/index.html", {
    "posts": posts,
    "page_obj": page_obj
})



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def profile(request, profile_id):

    user = User.objects.get(id=profile_id)
    posts = reversed(user.uploader.all())


    if request.method == "GET":
        try:
            followers_ = user.followers.filter(user_id= request.user).exists()
        except TypeError:
            return render(request, "network/profile.html", {
                "current_user": user,
                "posts": posts
            })

        return render(request, "network/profile.html", {
            "current_user": user,
            "posts": posts,
            "request_user": User.objects.get(id=request.user.id),
            "is_following": followers_
        })

    if request.method == "PUT":
        data = json.loads(request.body)

        if data["follow"] == True:
            # Follow user
            print("FOLLOWING")
            follower = User.objects.get(id=data["doing_following"])

            obj, created = UserFollowing.objects.get_or_create(user_id=follower, following_user_id=user)

            if created == False:
                return HttpResponse(status=204)
            obj.save()
            return HttpResponse(status=204)

        
        else:
            # Unfollow user
            print("DELETING FOLLOWING")
            obj = UserFollowing.objects.get(user_id=data["doing_following"], following_user_id=profile_id)
            obj.delete()
        
        return HttpResponse(status=204)



def following(request):

    followed_people = UserFollowing.objects.filter(user_id=request.user.id).values("following_user_id")
    posts = Post.objects.filter(post_creator__in=followed_people).order_by("-date")

    paginator = Paginator(posts, 10)

    page = request.GET.get("page")


    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "network/following.html", {
        "posts": posts,
        "page_obj": page_obj
    })




def posts(request):
    if request.method == "POST":
        print("POSTING")




    if request.method == "GET":

        posts = Post.objects.all().order_by("-date")

        paginator = Paginator(posts, 10)

        page = request.GET.get("page")

        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        print(page_obj)
        

        return render(request, "network/index.html", {
            "posts": posts,
            "page_obj": page_obj
        })


@csrf_exempt
def single_post(request, post_id):

    if request.method == "GET":    
        post = Post.objects.get(id=post_id)
        return JsonResponse(post.serialize())

    if request.method == "PUT":
        print (request.body)
        return HttpResponse(status=204)