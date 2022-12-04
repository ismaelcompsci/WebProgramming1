from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.load_wiki, name="load_wiki"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage", views.editpage, name="editpage")
]
