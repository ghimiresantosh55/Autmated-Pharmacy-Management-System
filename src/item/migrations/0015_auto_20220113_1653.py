# Generated by Django 3.1.9 on 2022-01-13 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0014_auto_20220109_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Max value  price can be upto 9999999999.99, price means MRP', max_digits=12),
        ),
    ]
