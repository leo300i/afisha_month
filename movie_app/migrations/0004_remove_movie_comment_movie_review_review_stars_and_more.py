# Generated by Django 4.0.5 on 2022-06-28 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0003_comment_movie_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='comment',
        ),
        migrations.AddField(
            model_name='movie',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movie_app.review'),
        ),
        migrations.AddField(
            model_name='review',
            name='stars',
            field=models.IntegerField(default=-1),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
