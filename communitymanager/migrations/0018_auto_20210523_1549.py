# Generated by Django 2.1.15 on 2021-05-23 15:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0017_auto_20210523_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_evenement',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name="Date de l'évenement"),
        ),
    ]
