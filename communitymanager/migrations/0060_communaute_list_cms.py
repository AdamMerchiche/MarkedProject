# Generated by Django 2.2 on 2021-06-06 14:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communitymanager', '0059_merge_20210602_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='communaute',
            name='list_CMs',
            field=models.ManyToManyField(blank=True, related_name='CMs', to=settings.AUTH_USER_MODEL),
        ),
    ]
