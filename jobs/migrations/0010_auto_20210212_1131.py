# Generated by Django 3.1 on 2021-02-12 06:01

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_auto_20210208_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='description',
            field=ckeditor.fields.RichTextField(default=None),
        ),
    ]
