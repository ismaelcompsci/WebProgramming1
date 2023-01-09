from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    path("stream", views.stream, name="stream"),



    # API
    path("stream/<str:channel>", views.get_stream, name="get_stream"),
    path("chatlogs", views.get_userlogs, name="logs")
]