# Generated by Django 3.1 on 2021-03-10 14:05

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210226_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='message',
            field=django_quill.fields.QuillField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='resume',
            field=django_quill.fields.QuillField(blank=True, verbose_name='Resume'),
        ),
    ]
