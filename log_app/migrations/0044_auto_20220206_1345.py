# Generated by Django 3.1.9 on 2022-02-06 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0043_auto_20220206_1313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loggenericname',
            old_name='archive',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='logitem',
            old_name='archive',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='logmedicinecategory',
            old_name='archive',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='logmedicineform',
            old_name='archive',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='logproductcategory',
            old_name='archive',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='logstrength',
            old_name='archive',
            new_name='archived',
        ),
        migrations.RenameField(
            model_name='logsupercategory',
            old_name='archive',
            new_name='archived',
        ),
    ]
