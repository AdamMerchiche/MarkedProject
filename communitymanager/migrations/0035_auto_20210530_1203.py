# Generated by Django 2.2 on 2021-05-30 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0034_auto_20210530_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
