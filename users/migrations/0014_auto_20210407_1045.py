# Generated by Django 3.1 on 2021-04-07 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20210310_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to='users/', verbose_name='image'),
        ),
    ]
