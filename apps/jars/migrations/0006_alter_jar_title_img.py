# Generated by Django 5.0 on 2024-01-05 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jars', '0005_alter_jar_options_alter_jartag_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jar',
            name='title_img',
            field=models.ImageField(blank=True, null=True, upload_to='jar_title_img'),
        ),
    ]