# Generated by Django 5.0 on 2024-01-12 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jars', '0010_amountofjar_incomes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountofjar',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time when sum was added.', verbose_name='date added'),
        ),
        migrations.AlterField(
            model_name='jaralbum',
            name='date_added',
            field=models.DateTimeField(auto_now=True, verbose_name='date added'),
        ),
    ]