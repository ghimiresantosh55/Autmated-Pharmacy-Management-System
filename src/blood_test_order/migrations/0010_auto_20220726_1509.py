# Generated by Django 3.2 on 2022-07-26 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_test_order', '0009_auto_20220726_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodtestordermain',
            name='is_blood_test',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='bloodtestordermain',
            name='is_test_package',
            field=models.BooleanField(blank=True),
        ),
    ]
