# Generated by Django 4.0.5 on 2022-06-16 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='director',
            old_name='Director',
            new_name='title',
        ),
    ]
