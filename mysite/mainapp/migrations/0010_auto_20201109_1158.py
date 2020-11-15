# Generated by Django 3.1.2 on 2020-11-09 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20201109_1144'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='firstname',
            field=models.CharField(default=1, max_length=255, verbose_name='Имя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='lastname',
            field=models.CharField(default=1, max_length=255, verbose_name='Фамилия'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='phone',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
