# Generated by Django 4.2.6 on 2023-11-20 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0018_legoset_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legoset',
            name='thumbnail',
            field=models.ImageField(upload_to=''),
        ),
    ]