# Generated by Django 5.1.1 on 2024-09-21 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college2', '0002_rename_woah_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video_expire',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='video_token',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
