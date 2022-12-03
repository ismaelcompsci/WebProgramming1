from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

class SearchTask(forms.Form):
    search = forms.CharField(label="search")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchTask()
    })

def check(request, name):
    names = util.list_entries()
    print(request.get_full_path())
    if name not in names:
        return render(request, "encyclopedia/error.html", {
            "error": name
        })



def all(request):
    page = request.get_full_path().split("/")[-1]
    q = page
    return render(request, f"encyclopedia/wiki/css.html", {
        "page": util.get_entry(q),
        "title": page,
        "form": SearchTask()
    })

def search(request):

    if request.method == "POST":

        data = SearchTask(request.POST)

        if data.is_valid():

            search = data.cleaned_data["search"]

            return HttpResponseRedirect(reverse(search))

        else:
            return render(request, "encyclopedia/index.html", {
                "form": data
            })
    else:

        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchTask()
    })





