# Generated by Django 3.2 on 2022-07-26 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blood_test_order', '0011_auto_20220726_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodtestordermain',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='bloodtestordermain',
            name='sub_total',
        ),
    ]
