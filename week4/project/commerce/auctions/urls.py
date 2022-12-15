from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("sell", views.sell, name="sell"),
    path("listing/<str:item_id>", views.listing, name="listing"),
    path("watchlist/<str:item_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<str:item_id>/bid", views.auction_bid, name="auction_bid"),
    path("listing/<str:item_id>/close", views.auction_close, name="auction_close"),
    path("categories", views.category_list, name="category_list"),
    path("category/<str:name>", views.category, name="category"),
    path("listing/<str:item_id>/comment", views.auction_comment, name="post_comment")
]
