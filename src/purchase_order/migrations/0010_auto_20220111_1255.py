# Generated by Django 3.1.9 on 2022-01-11 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0009_auto_20220110_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderdetail',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='purchaseorderdetail',
            name='discount_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Discount rate  default 0.00', max_digits=12),
        ),
        migrations.AddField(
            model_name='purchaseorderdetail',
            name='net_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
