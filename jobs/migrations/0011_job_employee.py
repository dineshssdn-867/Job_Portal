# Generated by Django 3.1 on 2021-02-22 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0010_auto_20210212_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='employee',
            field=models.ManyToManyField(blank=True, default=None, related_name='Job_Employee', to=settings.AUTH_USER_MODEL),
        ),
    ]
