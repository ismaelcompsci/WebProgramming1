from django.contrib.auth.models import AbstractUser
from django.db import models
from commerce.settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"



# Auction listing model
class Auction_item(models.Model):
    #user_id = models.IntegerField(default=1)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    url_image = models.URLField(default="")
    category = models.CharField(max_length=64, default="")

    # user who created item
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions", default=1)

    # people who have item in watchlist
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    #
    ended = models.BooleanField(default=False)

    def __str__(self):
        return f"Auction_item #{self.id}: {self.title} ({self.user.username})"




# Bid model
class Bid(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction_item, on_delete=models.CASCADE, related_name="bids")




# Comments on auction listing
class Comment(models.Model):
    message = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction_item, on_delete=models.CASCADE, related_name="comment")

    def __str__(self):
        return f"Comment #{self.id}: {self.user.username} on {self.auction.title}: {self.message}"