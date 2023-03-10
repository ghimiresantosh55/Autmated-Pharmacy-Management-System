# Generated by Django 3.1.9 on 2022-02-06 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0042_auto_20220201_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggenericname',
            name='archive',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
        migrations.AddField(
            model_name='logitem',
            name='archive',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
        migrations.AddField(
            model_name='logmedicinecategory',
            name='archive',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
        migrations.AddField(
            model_name='logmedicineform',
            name='archive',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
        migrations.AddField(
            model_name='logproductcategory',
            name='archive',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
        migrations.AddField(
            model_name='logstrength',
            name='archive',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
        migrations.AddField(
            model_name='logsupercategory',
            name='archive',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
    ]
