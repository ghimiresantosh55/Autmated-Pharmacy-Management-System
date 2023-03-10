# Generated by Django 3.1.9 on 2022-01-03 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0004_auto_20220103_1121'),
        ('log_app', '0005_logpurchaseorderdetail_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='logpurchaseorderdetail',
            name='ref_purchase_order_detail',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase_order.purchaseorderdetail'),
        ),
        migrations.AddField(
            model_name='logpurchaseordermain',
            name='ref_purchase_order_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase_order.purchaseordermain'),
        ),
    ]
