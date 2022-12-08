from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Auction listing model
class Auction_item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.FloatField()
    url_image = models.URLField(default="")
    category = models.CharField(max_length=64, default="")

    def __str__(self):
        return f"{self.title} selling for {self.starting_bid}"

# Bid model

# Comments on auction listing
