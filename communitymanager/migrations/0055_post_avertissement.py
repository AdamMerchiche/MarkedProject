# Generated by Django 2.2 on 2021-05-31 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0054_remove_communaute_ferme_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='avertissement',
            field=models.BooleanField(default=False),
        ),
    ]
