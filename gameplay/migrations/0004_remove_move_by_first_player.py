# Generated by Django 2.0.1 on 2018-01-21 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gameplay', '0003_auto_20180112_0353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='by_first_player',
        ),
    ]