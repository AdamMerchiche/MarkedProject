# Generated by Django 2.2 on 2021-05-30 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0035_auto_20210530_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
