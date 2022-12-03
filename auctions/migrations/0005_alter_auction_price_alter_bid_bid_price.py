# Generated by Django 4.0.1 on 2022-10-05 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auction_current_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='price',
            field=models.FloatField(error_messages={'name': {'max_length': 'The price must be between 0 and 999.99.'}}, help_text='Maximum 999.99', null=True),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_price',
            field=models.FloatField(blank='True', null='True'),
        ),
    ]