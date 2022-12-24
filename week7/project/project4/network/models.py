from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    likes = models.ForeignKey("Post", on_delete=models.CASCADE, null=True)




class Post(models.Model):
    # Creator of Post
    post_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploader")
    # Text
    text = models.CharField(max_length=255)
    # Date
    date = models.DateTimeField(default=datetime.now())
    # Likes
    likes = models.ManyToManyField(User, related_name="likers", default=0)


# Comments on Post
class Comment(models.Model):
    message = models.TextField(max_length=255)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment #{self.id}:"