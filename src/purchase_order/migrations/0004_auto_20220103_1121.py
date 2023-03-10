# Generated by Django 3.1.9 on 2022-01-03 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0003_purchaseorderdetail_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderdetail',
            name='ref_purchase_order_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='purchase_order.purchaseorderdetail'),
        ),
        migrations.AddField(
            model_name='purchaseordermain',
            name='ref_purchase_order_main',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='purchase_order.purchaseordermain'),
        ),
    ]
