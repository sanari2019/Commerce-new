# Generated by Django 4.0.1 on 2022-11-24 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_rename_user_bid_bidder_remove_bid_time_sent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=models.TextField(blank=True, db_index=True),
        ),
    ]
