# Generated by Django 4.2.6 on 2023-11-04 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0008_legoset_averagerating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='legoset',
            old_name='averageRating',
            new_name='satisfactionRating',
        ),
        migrations.AddField(
            model_name='legoset',
            name='totalReviews',
            field=models.IntegerField(default=0),
        ),
    ]