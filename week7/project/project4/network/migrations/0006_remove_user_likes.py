# Generated by Django 4.1.3 on 2022-12-25 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0005_alter_post_date_alter_post_likes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="likes",
        ),
    ]
