# Generated by Django 3.1.9 on 2022-01-07 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_order', '0004_orderdetail_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetail',
            name='unit',
        ),
    ]
