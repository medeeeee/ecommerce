# Generated by Django 3.2 on 2021-07-15 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listing_closed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='closed',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='last_bid',
        ),
    ]