# Generated by Django 3.1.9 on 2022-02-18 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0032_item_ws_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='popriority',
            name='archived',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
    ]
