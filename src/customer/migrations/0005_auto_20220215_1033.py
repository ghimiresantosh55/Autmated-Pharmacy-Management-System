# Generated by Django 3.1.9 on 2022-02-15 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20220201_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='home_address',
            field=models.CharField(help_text='home address should be maximum of 255 characters', max_length=255),
        ),
    ]
