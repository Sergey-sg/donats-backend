# Generated by Django 5.0 on 2023-12-28 22:01

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monobank_id', models.CharField(help_text='ID of monobank jar', max_length=31, unique=True, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='jar id')),
                ('title', models.CharField(help_text='Name of jar specified by user', max_length=100, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='jar name')),
                ('goal', models.IntegerField(blank=True, help_text='A goal sum of jar', null=True, validators=[django.core.validators.MinValueValidator(0, "Value can't be less than 0")], verbose_name='goal')),
                ('active', models.BooleanField(null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, help_text='The date and time when jar was added to website.', verbose_name='date added')),
                ('date_closed', models.DateTimeField(blank=True, help_text='The date and time when goal sum in jar was reached.', null=True, verbose_name='date closed')),
            ],
            options={
                'verbose_name': 'jar',
                'verbose_name_plural': 'jars',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='JarTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of tag', max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='name')),
            ],
            options={
                'verbose_name': 'jar tag',
                'verbose_name_plural': 'jar tags',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='JarCurrentSum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.IntegerField(help_text='A current sum in jar', validators=[django.core.validators.MinValueValidator(0)])),
                ('jar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jars.jar', verbose_name='jar id')),
            ],
            options={
                'verbose_name': 'jar current sum',
                'verbose_name_plural': 'jar current sums',
                'ordering': ['sum'],
            },
        ),
        migrations.AddField(
            model_name='jar',
            name='tags',
            field=models.ManyToManyField(to='jars.jartag'),
        ),
    ]
