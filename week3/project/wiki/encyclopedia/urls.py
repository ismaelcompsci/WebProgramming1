from django.urls import path
from . import util
from . import views


pages = util.list_entries()




urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search")
]

for page in pages:
    urlpatterns.append(path(f"wiki/{page}", views.all, name=page.lower()))

urlpatterns.append(path("wiki/<str:name>",views.check))