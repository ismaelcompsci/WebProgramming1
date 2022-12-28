# Generated by Django 4.1.3 on 2022-12-25 21:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0006_remove_user_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="following",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]