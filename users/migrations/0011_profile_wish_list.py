# Generated by Django 3.1 on 2021-02-25 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_job_employee'),
        ('users', '0010_auto_20210225_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wish_list',
            field=models.ManyToManyField(blank=True, default=None, related_name='wish_list', to='jobs.Job'),
        ),
    ]
