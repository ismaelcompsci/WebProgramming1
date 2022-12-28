from django.contrib.auth.models import AbstractUser
from django.utils.timezone import make_aware
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"


        


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


