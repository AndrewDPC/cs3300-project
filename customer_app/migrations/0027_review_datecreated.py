# Generated by Django 4.2.6 on 2023-11-21 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_app', '0026_alter_review_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
