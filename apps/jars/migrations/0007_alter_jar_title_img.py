# Generated by Django 5.0 on 2024-01-05 17:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jars', '0006_alter_jar_title_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jar',
            name='title_img',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='title_img'),
        ),
    ]
