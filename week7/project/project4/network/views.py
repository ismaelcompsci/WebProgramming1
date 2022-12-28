from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .utils import *
from .models import *



def index(request):
    if request.method == "POST":
        post = post_maker(request, request.user)
        new_post = Post(post_creator=post["post_creator"], text=post["text"], date=post["date"])
        new_post.save()

    posts = reversed(Post.objects.all())
    
    return render(request, "network/index.html", {
    "posts": posts
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

    followers_ = user.followers.filter(user_id= request.user).exists()


    if request.method == "GET":
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
    posts = reversed(Post.objects.filter(post_creator__in=followed_people))

    return render(request, "network/following.html", {
        "posts": posts
    })







def posts(request):
    if request.method == "POST":
        print("POSTING")


    if request.method == "GET":
        posts = reversed(Post.objects.all())

        return render(request, "network/index.html", {
            "posts": posts
        })


@csrf_exempt
def single_post(request, post_id):
    print(post_id , request)
    print(request.body)
    
    post = Post.objects.get(id=post_id)
    print(post.post_creator)

    # if PUT if like true like
        # update like count on page
    # else dislike
        #update like count on page

    return HttpResponse(post.post_creator)