# Generated by Django 4.2.13 on 2024-06-25 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_remove_borrowrecord_returned_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowrecord',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]
