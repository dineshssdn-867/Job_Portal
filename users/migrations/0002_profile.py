# Generated by Django 2.1.15 on 2021-02-08 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/users')),
                ('birth_day', models.DateField(blank=True, default=None, null=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('resume', models.TextField(blank=True)),
                ('company', models.CharField(blank=True, max_length=250)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
