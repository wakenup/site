# Generated by Django 3.1.2 on 2020-11-03 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_tournament_finishedtour'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='islive',
            field=models.BooleanField(default=False),
        ),
    ]