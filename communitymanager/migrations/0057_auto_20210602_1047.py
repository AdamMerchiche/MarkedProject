# Generated by Django 2.2 on 2021-06-02 08:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0056_auto_20210601_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communaute',
            name='abonnes',
            field=models.ManyToManyField(blank=True, related_name='abonnes', to=settings.AUTH_USER_MODEL),
        ),
    ]