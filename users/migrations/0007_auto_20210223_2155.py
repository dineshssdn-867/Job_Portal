# Generated by Django 3.1 on 2021-02-23 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210223_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='media/users/gsmarena_001.jpg', upload_to='media/users', verbose_name='image'),
        ),
    ]
