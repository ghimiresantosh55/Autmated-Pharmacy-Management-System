# Generated by Django 3.2 on 2022-07-24 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_test', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodtest',
            name='active',
            field=models.BooleanField(default=True, help_text='By default active=True'),
        ),
        migrations.AddField(
            model_name='bloodtestcategory',
            name='active',
            field=models.BooleanField(default=True, help_text='By default active=True'),
        ),
        migrations.AddField(
            model_name='testpackage',
            name='active',
            field=models.BooleanField(default=True, help_text='By default active=True'),
        ),
    ]
