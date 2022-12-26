
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_id>", views.profile, name="profile"),









    # API
    # all Posts 
    path("posts", views.posts, name="posts"),
    # single post
    path("posts/<int:post_id>", views.single_post, name="single_post")
]


    # # API Routes
    # path("posts", views.compose, name="compose"),
    # path("posts/<int:post_id>", views.email, name="email"),
    # path("post/<str:mailbox>", views.mailbox, name="mailbox"),