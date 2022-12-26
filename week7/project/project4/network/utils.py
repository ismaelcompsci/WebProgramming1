from datetime import datetime
from django.conf import settings
from .models import *

def post_maker(request, user):

    n_time = datetime.now()
    settings.TIME_ZONE
    a_time = make_aware(n_time)
    
    post = {}
    # Username of poster
    post["post_creator"] = user
    # Post Content
    post["text"] = request.POST["post-text"]
    # Post Date
    post["date"] = a_time
    # Likes

    return post