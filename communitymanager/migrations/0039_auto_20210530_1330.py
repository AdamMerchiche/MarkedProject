# Generated by Django 2.2 on 2021-05-30 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0038_auto_20210530_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentaire',
            name='visible',
        ),
        migrations.AddField(
            model_name='commentaire',
            name='invisible',
            field=models.BooleanField(default=False),
        ),
    ]