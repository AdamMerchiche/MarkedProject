# Generated by Django 2.2 on 2021-05-30 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0045_auto_20210530_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentaire',
            name='post',
            field=models.ForeignKey(on_delete='models.PROTECT', to='communitymanager.Post'),
        ),
    ]
