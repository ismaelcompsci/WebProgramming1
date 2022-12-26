from django.contrib.auth.models import AbstractUser
from django.utils.timezone import make_aware
from django.db import models
from datetime import datetime


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, null=True)
    followers = models.ManyToManyField("self", blank=True, null=True)



class Post(models.Model):
    # Creator of Post
    post_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploader")
    # Text
    text = models.CharField(max_length=255)
    # Date
    date = models.DateTimeField(default=datetime.now)
    # Likes
    likes = models.ManyToManyField(User, related_name="likers", default=None, null=True)

    def serialize(self):
        return {
            "creator": self.post_creator.username,
            "text":self.text,
            "date":self.date,
            "likes":[user.username for user in self.likes],
        }


# Comments on Post
class Comment(models.Model):
    message = models.TextField(max_length=255)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment #{self.id}:"


