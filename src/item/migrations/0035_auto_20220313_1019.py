# Generated by Django 3.1.9 on 2022-03-13 04:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0034_auto_20220222_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='free_qty',
            field=models.IntegerField(blank=True, help_text='Null= True, blank =True', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='item',
            name='purchase_qty',
            field=models.IntegerField(blank=True, help_text='Null= True, blank =True', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]