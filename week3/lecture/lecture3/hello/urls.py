from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bi", views.bi, name="bi"),
    path("david", views.david, name="david"),
    path("<str:name>", views.greet, name="greet")
]