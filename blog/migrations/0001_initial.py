# Generated by Django 3.1 on 2021-02-27 05:51

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('tweet', ckeditor.fields.RichTextField(blank=True, max_length=500, verbose_name='Resume')),
                ('date', models.DateField(auto_now_add=True, verbose_name='date')),
                ('image', models.ImageField(default='media/happy_blog/images.png', upload_to='media/blog', verbose_name='image')),
            ],
        ),
    ]
