# Generated by Django 3.1.9 on 2022-01-02 05:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0002_auto_20211229_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logitem',
            old_name='item_image',
            new_name='image',
        ),
    ]
