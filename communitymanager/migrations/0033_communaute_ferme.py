# Generated by Django 2.2 on 2021-05-29 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0032_communaute_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='communaute',
            name='ferme',
            field=models.BooleanField(default=False),
        ),
    ]