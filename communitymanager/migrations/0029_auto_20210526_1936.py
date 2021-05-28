# Generated by Django 2.1.15 on 2021-05-26 19:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('communitymanager', '0028_auto_20210525_1945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date_creation']},
        ),
        migrations.AlterField(
            model_name='post',
            name='date_creation',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date du post'),
        ),
    ]