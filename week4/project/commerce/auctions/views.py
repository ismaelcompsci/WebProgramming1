from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Auction_item, Bid, Category, Comment


def index(request):
    items = Auction_item.objects.all()
    return render(request, "auctions/index.html", {"items": items})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, item_id):
    if not request.user.is_authenticated:
        return redirect(login_view)

    # check if item in users watchlist
    auction_check = Auction_item.objects.get(id=item_id)
    watchlist_check = request.user.watchlist

    if auction_check in watchlist_check.all():
        return render(
            request,
            "auctions/listing.html",
            {"listing": auction_check, "delete_button": True},
        )

    auction = Auction_item.objects.get(id=item_id)
    
    return render(request, "auctions/listing.html", 
    {
        "listing": auction,
        "comments": Comment.objects.filter(auction=auction)
    })


# Create Listing
def sell(request):
    if not request.user.is_authenticated:
        return redirect(login_view)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        url = request.POST["url"]
        category = Category(name=request.POST["category"])

        auction_item = Auction_item(
            title=title,
            description=description,
            starting_bid=bid,
            url_image=url,
            category=category,
            user=request.user,
        )
        category.save()
        auction_item.save()
        # Auction_item.objects.create(auction_item)

    return render(request, "auctions/sell.html")


def watchlist_add(request, item_id):
    if request.method == "POST":

        auction = Auction_item.objects.get(id=item_id)
        watchlist = request.user.watchlist

        if auction in watchlist.all():
            print("Removing item from list")
            watchlist.remove(auction)
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": Auction_item.objects.get(id=item_id),
                },
            )
        else:
            print("Adding to Watchlist")
            watchlist.add(auction)

    return render(
        request,
        "auctions/listing.html",
        {"listing": Auction_item.objects.get(id=item_id), "delete_button": True},
    )

def auction_bid(request, item_id):
    auction = Auction_item.objects.get(id=item_id)
    user = request.user
    new_bid = float(request.POST["bid"])
    current_bids = Bid.objects.filter(auction=auction)


    is_highes_bid = all(new_bid > n.amount for n in current_bids)
    is_valid_first_bid = new_bid >= auction.starting_bid

    if is_highes_bid and is_valid_first_bid:        
        bid = Bid(amount=new_bid, user=user, auction=auction)
        bid.save()
    
    url = reverse("listing", kwargs={"item_id":item_id})

    return HttpResponseRedirect(url)


# User should have the ability to close a auction if he created it
def auction_close(request, item_id):
    print(request.POST)
    auction = Auction_item.objects.get(id=item_id)

    print(auction.ended)

    if request.user == auction.user:
        auction.ended = True
        auction.save()
    
    return HttpResponseRedirect(reverse("listing", kwargs={"item_id":item_id}))


# Users signed in should be able to add comments
def auction_comment(request, item_id):
    comment = request.POST["comment"]
    post_user = request.user
    auction = Auction_item.objects.get(id=item_id)

    if request.method == "POST":
        c = Comment(user=post_user, message=comment, auction=auction)
        c.save()

    url = reverse('listing', kwargs={'item_id': item_id})
    return HttpResponseRedirect(url)

         


def watchlist(request):
    if not request.user.is_authenticated:
        redirect(login_view)

    return render(
        request,
        "auctions/index.html",
        {
            "items": request.user.watchlist.all(),
        },
    )

def category_list(request):
    return render(request, "auctions/category_list.html", {
        "categories": Category.objects.all()
    })


def category(request, name):
    category = Category.objects.get(name=name)

    aucitons = Auction_item.objects.filter(
        category=category
    )

    return render(request, "auctions/index.html", {
        "items": aucitons,
        "title": category.name
    })









