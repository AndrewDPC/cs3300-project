# Generated by Django 4.2.6 on 2023-11-03 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0004_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='legoset',
            name='averageRating',
            field=models.IntegerField(default=0),
        ),
    ]