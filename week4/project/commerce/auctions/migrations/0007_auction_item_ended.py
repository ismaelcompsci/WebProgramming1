# Generated by Django 4.1.3 on 2022-12-13 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_alter_auction_item_starting_bid_comment_bid"),
    ]

    operations = [
        migrations.AddField(
            model_name="auction_item",
            name="ended",
            field=models.BooleanField(default=False),
        ),
    ]
