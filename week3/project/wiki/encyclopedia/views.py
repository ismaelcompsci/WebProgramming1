from django.shortcuts import render
from markdown2 import Markdown
import markdown2
from . import util


markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def load_wiki(request, name):

    entries = util.get_entry(name)

    if not entries:
        return render(request, "encyclopedia/error.html", {
            "title": name
    })

    return render(request, "encyclopedia/load_wiki.html", {
        "title": name,
        "info": markdown2.markdown(entries)
    })


def search(request):


    if request.method == "POST":
        title = request.POST["q"]
        
        checker = substring_checker(title)

        bl, pg = exists(title)

        if checker:
            return render(request, "encyclopedia/substring.html",{
                "entries": checker
            })

        if bl == False or not checker:
            return render(request, "encyclopedia/error.html", {
                "title": title
            })

        return render(request, "encyclopedia/load_wiki.html", {
            "title": title,
            "info": util.get_entry(pg)
            })



def newpage(request):
    if request.method == "POST":
        title, textarea = request.POST["title"], request.POST["textarea"]
        
        bl, pg = exists(title)

        if bl == True:
            return render(request, "encyclopedia/error.html", {
                "title": title,
                "Error": "Already Exists"
            })

        util.save_entry(title, textarea)

        return render(request, "encyclopedia/load_wiki.html", {
            "title": title,
            "info": util.get_entry(title)
        })
    return render(request, "encyclopedia/newpage.html")




def editpage(request):

    if request.method == "GET":
        refer = request.META.get('HTTP_REFERER').split("/")[-1]

        data = util.get_entry(refer)

        return render(request, "encyclopedia/editpage.html", {
            "title": refer,
            "data": data
        })
    


    if request.method == "POST": 
        print(request.POST)

        info = request.POST["textarea"]
        title  = request.POST["title"]

        util.save_entry(title, info)

        print(title, info)

        return render(request, "encyclopedia/load_wiki.html", {
        "title": title,
        "info": util.get_entry(title)
        })












def substring_checker(search):
    pages = util.list_entries()
    hit = []

    for page in pages:
        if page.find(search.upper()) != -1 or page.find(search.lower()) != -1:
            hit.append(page)
            print(page)
    return hit


def exists(search):
    pages = util.list_entries()

    for page in pages:
        if search.lower() == page.lower():
            print(page)
            return True, page
    return False, None