# Generated by Django 3.1.9 on 2022-01-26 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0004_auto_20220120_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(help_text='Address can be max. of 150 character', max_length=150),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone_no',
            field=models.CharField(help_text='Phone no. can be max. of 30 characters', max_length=30),
        ),
    ]
