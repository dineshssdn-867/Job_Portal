# Generated by Django 3.1 on 2021-02-26 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happy_blog', '0002_auto_20210226_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='happy_blog',
            name='image',
            field=models.ImageField(default='media/users/images.png', upload_to='happy_blog', verbose_name='image'),
        ),
    ]
